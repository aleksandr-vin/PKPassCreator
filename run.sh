#!/usr/bin/env bash

python main.py --certificate-password $(<Certificates-pass)  \
  --pass-type-identifier  pass.com.aleksandr.vin.uas.pilot.lic \
  --team-identifier DYBARU2854 \
  --certificate-path Certificates.p12 \
  --wwdr-path WWDR.pem
