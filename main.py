import json
import hashlib
import os
import sys
import shutil
from typing import Callable, Optional
from zipfile import ZipFile

from pass_dict import pass_dict

KEY_PASSWORD = "password"
WWDR_PATH = "WWDR.pem"
CERTIFICATE_PATH = "certificates.p12"
PASS_TYPE_IDENTIFIER = "com.apple.application-password"
TEAM_IDENTIFIER = "2V9Z6R8X2R"
PK_PASS_NAME = "Generic"
OPENSSL_APP = "openssl"

SUPPORTED_ASSET_FILES = [
    "icon.png",
    "icon@2x.png",
    "background.png",
    "background@2x.png",
    "logo.png",
    "logo@2x.png",
    "footer.png",
    "footer@2x.png",
    "strip.png",
    "strip@2x.png",
    "thumbnail.png",
    "thumbnail@2x.png",
]

def with_clean_up(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(e)
        finally:
            generated_files = [
                "pass.json",
                "manifest.json",
                "passcertificate.pem",
                "passkey.pem",
                "signature",
            ]

            for asset_file in SUPPORTED_ASSET_FILES + generated_files:
                if os.path.exists(asset_file):
                    os.remove(asset_file)
    return wrapper

@with_clean_up
def main():
    pass_dict_copy = create_pass_dict(
        pass_type_identifier=PASS_TYPE_IDENTIFIER,
        team_identifier=TEAM_IDENTIFIER,
    )
    pass_dict_json = json.dumps(pass_dict_copy, indent=2)
    with open("pass.json", "w") as f:
        f.write(pass_dict_json)

    create_manifest_json(asset_path=f"{PK_PASS_NAME}.pass")

    certificate_password: Optional[str] = None
    skip_next_value = False
    for index, arg in enumerate(sys.argv[1:]):
        if skip_next_value:
            skip_next_value = False
            continue
        match arg:
            case "--cert-pass":
                if index + 1 < len(sys.argv[index:]):
                    certificate_password = sys.argv[index + 2]
                    skip_next_value = True
                else:
                    print("--cert-pass requires a password")

    if not certificate_password:
        certificate_password = input("what is the password of the provided certificate?\n")
        return

    #  Create pass certificate
    os_code = os.system(f"{OPENSSL_APP} pkcs12 -in {CERTIFICATE_PATH} -clcerts -nokeys -out passcertificate.pem -passin pass:{certificate_password}")
    if os_code != 0:
        print("Error creating pass certificate")
        return
    # Create pass key
    os_code = os.system(f"{OPENSSL_APP} pkcs12 -in {CERTIFICATE_PATH} -nocerts -out passkey.pem -passin pass:{certificate_password} -passout pass:{KEY_PASSWORD}")
    if os_code != 0:
        print("Error creating pass key")
        return
    # Create signature
    os_code = os.system(f"{OPENSSL_APP} smime -binary -sign -certfile {WWDR_PATH} -signer passcertificate.pem -inkey passkey.pem -in manifest.json -out signature -outform DER -passin pass:{KEY_PASSWORD}")
    if os_code != 0:
        print("Error creating signature")
        return

    asset_files_to_delete = [
        "passkey.pem",
        "passcertificate.pem",
        "signature",
        "pass.json",
    ]
    asset_files = [
        "signature",
        "pass.json",
        "manifest.json",
    ]

    for (_, _, filenames) in os.walk(f"{PK_PASS_NAME}.pass"):
        for filename in filenames:
            if filename in SUPPORTED_ASSET_FILES:
                shutil.copy2(f"{PK_PASS_NAME}.pass/{filename}", filename)
                asset_files_to_delete.append(filename)
                asset_files.append(filename)

    with ZipFile(f"{PK_PASS_NAME}.pkpass", "w") as zip_file:
        for asset_file in asset_files:
            zip_file.write(asset_file)

    os_code = os.system(f"open {PK_PASS_NAME}.pkpass")
    if os_code != 0:
        print("Error opening pass")
        return



def create_manifest_json(asset_path: str):
    with open("pass.json", "r") as f:
        pass_json = f.read()

    hashed_pass_json = hashlib.sha1(pass_json.encode('utf-8')).hexdigest()

    manifest_dict = {"pass.json": hashed_pass_json}

    for (_, _, filenames) in os.walk(asset_path):
        for filename in filenames:
            if filename in SUPPORTED_ASSET_FILES:
                manifest_dict[filename] = hashlib.sha1(
                    open(f"{asset_path}/{filename}", "rb").read()
                ).hexdigest()

    with open(f"manifest.json", "w") as f:
        f.write(json.dumps(manifest_dict, indent=4))


def create_pass_dict(pass_type_identifier: str, team_identifier: str):
    pass_dict_copy = pass_dict.copy()
    pass_dict_copy["passTypeIdentifier"] = pass_type_identifier
    pass_dict_copy["teamIdentifier"] = team_identifier
    return pass_dict_copy


main()
