import setuptools

setuptools.setup(
    name="revengedit",
    description="edit level difficulty settings in Zuma's Revenge! *.dat files",
    author="Shambles_SM",
    packages=["revengedit"],
    entry_points={"console_scripts": ["revengedit = revengedit.__main__:main"]}
)