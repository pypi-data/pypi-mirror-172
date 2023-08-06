from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Python Package Übung für den PyPI"

setup(
    name="etpyfi_uebung_jochen",
    version=VERSION,
    author="Thomas Benkenstein",
    author_email="thomas.benkenstein@experteach.de",
    description=DESCRIPTION,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True, # alles, was sich im package Ordner befindet wird hochgeladen
    #package_data=["requirements.txt"],
    install_requires=["requests", "aiofiles"], # welche Module braucht mein Modul, diese müssen vorhanden sein sucht im Sideindex der Installation lokal
    keywords=["python", "code"], # um was geht es in meinem Package/Modul
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux", # letztes Comma ist laut PEP8 zwingend, von Python ausführung aber nicht zwingend,
        # bei jeder Aufzählung sollte man mit einem Komma abschließen
    ], # https://pypi.org/classifiers # Liste von Classifiers, die man nutzen kann, um das Package besser auffindbar zu machen
        # trailing Komma hinter einer Angabe, Formater black könnte man nutzen, finden Python Enthusiasten spitze ;-)
)