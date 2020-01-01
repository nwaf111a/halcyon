del final.min.py
del final.min.obf.py
pyminifier -o final.min.py final.py 
pyminifier -o final.min.obf.py  --obfuscate-functions --obfuscate-classes --obfuscate-import-methods --replacement-length=5 final.min.py
pause