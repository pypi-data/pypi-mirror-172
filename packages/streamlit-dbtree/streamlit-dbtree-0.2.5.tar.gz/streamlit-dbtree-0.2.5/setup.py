from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-dbtree",
    #begin 
    version="0.2.5", 
    #end
    author="Anthony Alteirac",
    author_email="anthony@alteirac.com",
    description="Visualize Snowflake DB tree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=["streamlit>=1.2", "jinja2","snowflake-connector-python"],
)
