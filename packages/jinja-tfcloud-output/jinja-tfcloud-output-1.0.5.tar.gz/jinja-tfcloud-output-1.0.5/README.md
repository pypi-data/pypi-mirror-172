# Jinja Terraform Output

An extension to the jinja2 templating engine that allows you to access the outputs of a terraform workspace

## Install

```sh
pip3 install jinja-tfcloud-output
```

## Usage

```jinja2
# template.j2
Output {% terraform_query "tf-output-name" %}
