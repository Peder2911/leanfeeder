
import setuptools

with open("README.md") as f:
    long_description=f.read()

setuptools.setup(
        name = "leanfeeder",
        version = "0.0.1",
        author = "Peder G. Landsverk",
        author_email = "pglandsverk@gmail.com",
        description = "Tool for pushing data to a Postgres DB without too much hassle.",
        long_description = long_description,
        long_description_content_type="test/markdown",
        url = "https://www.github.com/peder2911/leanfeeder",
        packages = setuptools.find_packages(),
        scripts=["bin/leanfeeder"],
        python_requires=">=3.7",
        install_requires=[
            "strconv==0.4.2",
            "psycopg2==2.8.6",
            "fire==0.3.1"
        ])
