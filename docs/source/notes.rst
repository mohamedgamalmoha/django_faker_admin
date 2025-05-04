Important Notes
===============

.. warning::
   This package is a work in progress, and not all features are implemented yet (CLI, configurations for each model, etc.).

Development Status
------------------

Django Faker Admin is currently in active development. Please be aware of the following limitations:

* **Not Production Ready**: This package is designed to help create data in testing and development environments. It should **not** be used in production environments.

* **Single Model Focus**: The package has been primarily tested with standalone single models. Using it with related models across different database tables may lead to unexpected behavior.

* **Planned Features**: Several features are planned but not yet implemented, including:
  
  * Command-line interface (CLI) tools
  * More granular configuration options for individual models
  * Advanced relationship handling
  * Data generation templates and presets

Contributing
------------

We welcome contributions from the community! If you have prior experience with Django, please feel free to contribute by:

* Opening issues for bugs or feature requests
* Submitting pull requests with improvements
* Helping with documentation
* Sharing examples of how you use the package

To contribute, please dont hesitate to reach out via our GitHub repository. We appreciate any help you can provide!

Feedback
--------

If you encounter any issues or have suggestions for improvements, please open an issue on our GitHub repository. Your feedback is invaluable in helping us improve Django Faker Admin.

Roadmap
-------

Our planned development roadmap includes:

1. Improved handling of model relationships
2. Command-line interface for generating data without using the admin interface
3. More configuration options for individual model fields
4. Pre-defined data generation templates
5. Performance optimizations for generating large datasets
6. Create factory for a given model, without passing it explicitly.

Stay tuned for updates as we continue to develop and enhance this package.
