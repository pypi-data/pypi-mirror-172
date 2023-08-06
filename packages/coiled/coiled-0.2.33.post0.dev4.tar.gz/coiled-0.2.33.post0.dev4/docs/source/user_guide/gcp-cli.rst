GCP Quickstart
~~~~~~~~~~~~~~

It's quick and easy to get started using Coiled in your own Google Cloud account.
This guide will cover the steps for getting started with Coiled
using the command-line interface, all from your terminal.

#. Install the Coiled Python library with::

    conda install -c conda-forge coiled-runtime python=3.9

   **or**::

    pip install coiled-runtime

#. Log in to your Coiled account::

    coiled login

#. Set up IAM::

    coiled setup gcp

   With your permission, this command will create the IAM roles and service accounts Coiled needs so you can create clusters in your GCP project. You will be prompted with an explanation at each step, so you can choose to say "yes" (or "no") at any point (see :doc:`gcp_configure` for more details).

   If you would like to use a custom network configuration or container registry, you can use the CLI tool to create the necessary service accounts in your GCP project::

    coiled setup gcp --manual-final-setup

   After which you will be provided with the required access key and prompted to complete configuration in the Coiled web app at ``https://cloud.coiled.io/<your-account>/settings/setup/update-backend-options``.

#. Start your Dask cluster in the cloud (see :ref:`Running your computation <first-computation>`)::

    ipython
    > import coiled
    > cluster = coiled.Cluster(name="gcp-quickstart", n_workers=5)

If you don't already an GCP account and have more questions, see :ref:`Need a cloud provider account? <no-cloud-provider>`

Coiled makes it easy to deploy clusters in a way that's secure by default.
If you have questions about how we handle security, see our documentation about :doc:`security` (or :doc:`talk to us <support>`!).