from setuptools import setup, find_packages


if __name__ == "__main__":
    setup(
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        include_package_data=False,
        package_data={
            "django_faker_admin": [
                "templates/**/*.html",
            ],
        }
    )
