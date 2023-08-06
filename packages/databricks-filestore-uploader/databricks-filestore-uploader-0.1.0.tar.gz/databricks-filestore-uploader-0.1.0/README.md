# **Databricks FileStore Uploader**
*A convenience tool for uploading local directories to the DBFS FileStore*

<br />

## **Upload Local Files**
This tool uploads specified source directories to specified paths in the *<abbr title="Databricks File System">DBFS</abbr> FileStore*.

Create a file adjacent to `main.py` called `input.yml`, and copy the following:
```yml
host : <workspace-url>
token: <user-access-token>

# THIS TOOL CREATES OR OVERWRITES THE TARGET FOLDER!
# Folder paths don't start with './'
# Folder paths don't end with '/'
payloads:
  some-local-folder : some-filestore-folder
  some-other-local-folder : some-other/filestore-folder
  # ...
```

Replace `<user-access-token>` with your token in databricks, and replace the example text under `payloads:` one or more "*source : destination*" pairs. \
These local source directory paths **are relative to `main.py`**.

You can then upload all files contained in the local source folders to their specified destinations with:
```
./main.py
```
Though make sure you have [PyYAML](https://pypi.org/project/PyYAML/) installed.

<br />

## **Verify Uploads**
In a databricks notebook, you can verify uploads with:
```py
display(dbutils.fs.ls("/FileStore/some-filestore-folder"))
```

<br />

> Please Note❗ \
> This tool CREATES or OVERWRITES it's target dbfs:/FileStore path. Only target folders that are meant to be overwritten, or don't exist.