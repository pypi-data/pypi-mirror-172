Helper package for coding and automation

**Version 0.1.9**

+ add dependencies requirement.txt

**Version 0.1.8**

Fix bugs:

+ [performance] instead of inserting directly new rows into table dataframe, first insert it into in-memory `row_pool_dict`, that fill data in that dict into the actual dataframe when needed.

---

**Version 0.1.7**

Fix bugs:

+ fix insert into table so slow by allowing insert multiple rows at once

---

**Version 0.1.6**

New features:

+ add DFCreator for manipulating table (DataFrame) - create, insert row, display, write to file

---

**Version 0.1.5**

New Features

+ add cmd module
+ new package structure

---

**Version 0.1.4**

New Features

+ add support to create Bitbucket Project from template

---

**Version 0.1.2**

New Features

+ add support to upload local to google drive.
