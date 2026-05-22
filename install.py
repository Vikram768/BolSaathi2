import argostranslate.package

# Available packages list
available_packages = argostranslate.package.get_available_packages()

# en → hi model install
for pkg in available_packages:
    if pkg.from_code == "en" and pkg.to_code == "hi":
        print("Downloading model...")
        download_path = pkg.download()
        print("Installing model...")
        argostranslate.package.install_from_path(download_path)

print("Done ✅")