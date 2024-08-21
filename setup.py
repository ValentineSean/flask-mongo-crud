from setuptools import setup, find_packages

classifiers = [
	"Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS :: MacOS X",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
]

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flask-mongo-crud",
    version="0.0.24",
    description="Automatically generates CRUD endpoints from defined models",
    # long_description=open("README.txt").read() + "\n\n" + open("CHANGELOG.txt").read(),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="",
    author="Valentine Sean Chanengeta",
    author_email="",
    license="MIT",
    classifiers=classifiers,
    keywords=[
        "flask-crud",
        "flask-mongo-crud",
        "flask-mongo-odm",
        "flask-mongo-orm",
	],
    packages=find_packages(),
    install_requires=[
        "blinker==1.6.2",
		"click==8.1.7",
		"colorama==0.4.6",
		"dnspython==2.4.2",
		"executing==2.0.0",
		"Flask==3.0.0",
		"Flask-PyMongo==2.3.0",
		"itsdangerous==2.1.2",
		"Jinja2==3.1.2",
		"MarkupSafe==2.1.3",
		"pymongo==4.5.0",
		"python-dotenv==1.0.0",
		"varname==0.12.0",
		"Werkzeug==3.0.0",
	]
)