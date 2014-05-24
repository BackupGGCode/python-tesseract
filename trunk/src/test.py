import subprocess
def getTesseractVersion():
	result=subprocess.check_output("tesseract -v".split(),stderr=subprocess.STDOUT)
	for item in result.split("\n"):
		subItems=item.split()
		if len(subItems)!=2:
			continue
		name, version=subItems
		if name.strip().lower()=="tesseract":
			return version.strip()

	return None

print getTesseractVersion()
