<details open>
<summary><h1>generalpackager</h1></summary>

Tools to interface GitHub, PyPI, NPM and local modules / repos. Used for generating files to keep projects dry and synced. Tailored for my general packages.

<details>
<summary><h2>Table of Contents</h2></summary>

<pre>
<a href='#generalpackager'>generalpackager</a>
├─ <a href='#Dependency-Diagram-for-ManderaGeneral'>Dependency Diagram for ManderaGeneral</a>
├─ <a href='#Installation-showing-dependencies'>Installation showing dependencies</a>
├─ <a href='#Information'>Information</a>
├─ <a href='#Attributes'>Attributes</a>
├─ <a href='#Contributions'>Contributions</a>
└─ <a href='#Todo'>Todo</a>
</pre>
</details>


<details open>
<summary><h2>Dependency Diagram for ManderaGeneral</h2></summary>

```mermaid
flowchart LR
2([file]) --> 4([packager])
1([library]) --> 2([file])
0([import]) --> 2([file])
1([library]) --> 3([vector])
1([library]) --> 4([packager])
0([import]) --> 1([library])
click 0 "https://github.com/ManderaGeneral/generalimport"
click 1 "https://github.com/ManderaGeneral/generallibrary"
click 2 "https://github.com/ManderaGeneral/generalfile"
click 3 "https://github.com/ManderaGeneral/generalvector"
click 4 "https://github.com/ManderaGeneral/generalpackager"
style 4 fill:#482
```
</details>


<details open>
<summary><h2>Installation showing dependencies</h2></summary>

| `pip install`                                                                      | `generalpackager`   |
|:-----------------------------------------------------------------------------------|:--------------------|
| <a href='https://pypi.org/project/generallibrary[table]'>generallibrary[table]</a> | ✔️                  |
| <a href='https://pypi.org/project/generalfile'>generalfile</a>                     | ✔️                  |
| <a href='https://pypi.org/project/gitpython'>gitpython</a>                         | ✔️                  |
| <a href='https://pypi.org/project/pygithub'>pygithub</a>                           | ✔️                  |
| <a href='https://pypi.org/project/requests'>requests</a>                           | ✔️                  |
| <a href='https://pypi.org/project/pyinstaller'>pyinstaller</a>                     | ✔️                  |
| <a href='https://pypi.org/project/coverage'>coverage</a>                           | ✔️                  |
</details>


<details open>
<summary><h2>Information</h2></summary>

| Package                                                              | Ver                                                | Latest Release        | Python                                                                                                                                                                                  | Platform        | Cover   |
|:---------------------------------------------------------------------|:---------------------------------------------------|:----------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------|:--------|
| [generalpackager](https://github.com/ManderaGeneral/generalpackager) | [0.5.5](https://pypi.org/project/generalpackager/) | 2022-10-19 16:24 CEST | [3.8](https://www.python.org/downloads/release/python-380/), [3.9](https://www.python.org/downloads/release/python-390/), [3.10](https://www.python.org/downloads/release/python-3100/) | Windows, Ubuntu | 67.4 %  |
</details>



<details>
<summary><h2>Attributes</h2></summary>

<pre>
<a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/__init__.py#L1'>Module: generalpackager</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L12'>Class: GitHub</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L12'>Class: GitHub</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localmodule.py#L8'>Class: LocalModule</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L15'>Class: LocalRepo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager.py#L17'>Class: Packager</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/pypi.py#L26'>Class: PyPI</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L28'>Method: api_url</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L44'>Method: download</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L40'>Method: exists</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L96'>Method: get_description</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L64'>Method: get_owners_packages</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L83'>Method: get_topics</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L71'>Method: get_website</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L33'>Property: git_clone_command</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L37'>Property: pip_install_command</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L108'>Method: request_kwargs</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L102'>Method: set_description</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L89'>Method: set_topics</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L77'>Method: set_website</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L25'>Property: ssh_url</a> <b>(Untested)</b>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L21'>Property: url</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localmodule.py#L8'>Class: LocalModule</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L12'>Class: GitHub</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localmodule.py#L8'>Class: LocalModule</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L15'>Class: LocalRepo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager.py#L17'>Class: Packager</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/pypi.py#L26'>Class: PyPI</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localmodule.py#L26'>Method: exists</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localmodule.py#L67'>Method: get_all_local_modules</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localmodule.py#L89'>Method: get_dependants</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localmodule.py#L74'>Method: get_dependencies</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localmodule.py#L20'>Property: module</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localmodule.py#L41'>Property: objInfo</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/#L426'>Property: path</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L15'>Class: LocalRepo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L12'>Class: GitHub</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localmodule.py#L8'>Class: LocalModule</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L15'>Class: LocalRepo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager.py#L17'>Class: Packager</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/pypi.py#L26'>Class: PyPI</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_target.py#L7'>Class: Targets</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L59'>Method: exists</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L135'>Method: format_file</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L88'>Method: get_examples_path</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L60'>Method: get_exeproduct_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L56'>Method: get_exetarget_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L52'>Method: get_generate_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L16'>Method: get_git_exclude_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L64'>Method: get_git_ignore_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L72'>Method: get_index_js_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L44'>Method: get_init_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L28'>Method: get_license_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L24'>Method: get_manifest_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L12'>Method: get_metadata_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L68'>Method: get_npm_ignore_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L8'>Method: get_org_readme_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L80'>Method: get_package_json_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L89'>Method: get_package_paths_gen</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L84'>Method: get_pre_commit_hook_path</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L48'>Method: get_randomtesting_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L4'>Method: get_readme_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L20'>Method: get_setup_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L76'>Method: get_test_js_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L36'>Method: get_test_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L75'>Method: get_test_paths</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L40'>Method: get_test_template_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_paths.py#L32'>Method: get_workflow_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L97'>Method: git_changed_files</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L65'>Property: gitpython_repo</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_target.py#L23'>Method: is_django</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_target.py#L27'>Method: is_exe</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_target.py#L19'>Method: is_node</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_target.py#L15'>Method: is_python</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L32'>Property: metadata</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L47'>Method: metadata_exists</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L69'>Method: repo_exists</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L41'>Property: target</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_target.py#L54'>Method: targetted</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L82'>Method: text_in_tests</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/node/localrepo_node.py#L6'>Class: LocalRepo_Node</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/python/localrepo_python.py#L11'>Class: LocalRepo_Python</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/python/localrepo_python.py#L25'>Method: get_python_exe_path</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/python/localrepo_python.py#L16'>Method: get_venv_path</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/python/localrepo_python.py#L30'>Method: unittest</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager.py#L17'>Class: Packager</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L12'>Class: GitHub</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localmodule.py#L8'>Class: LocalModule</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L15'>Class: LocalRepo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager.py#L17'>Class: Packager</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/other/packages.py#L9'>Class: Packages</a>
│  │  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/other/packages.py#L33'>Method: all_packages</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/pypi.py#L26'>Class: PyPI</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_target.py#L7'>Class: Targets</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L75'>Method: all_files_by_relative_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_github.py#L23'>Method: commit_and_push</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L172'>Method: compare_local_to_github</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L180'>Method: compare_local_to_pypi</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L113'>Method: create_blank_locally_python</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_github.py#L58'>Method: create_github_repo</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_github.py#L73'>Method: create_master_branch</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_github.py#L52'>Method: enable_vcs_operations</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L79'>Method: file_by_relative_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L91'>Property: file_secret_readme</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L43'>Property: files</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L151'>Method: filter_relative_filenames</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_relations.py#L65'>Method: general_bumped_set</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_relations.py#L71'>Method: general_changed_dict</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L370'>Method: generate_generate</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L247'>Method: generate_git_exclude</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L409'>Method: generate_index_js</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L354'>Method: generate_init</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L253'>Method: generate_license</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L454'>Method: generate_localfiles</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L238'>Method: generate_manifest</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L403'>Method: generate_npm_ignore</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L433'>Method: generate_package_json</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L331'>Method: generate_personal_readme</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L381'>Method: generate_pre_commit</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L362'>Method: generate_randomtesting</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L290'>Method: generate_readme</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L187'>Method: generate_setup</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L418'>Method: generate_test_node</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L393'>Method: generate_test_python</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L267'>Method: generate_workflow</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_markdown.py#L230'>Method: get_attributes_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_markdown.py#L14'>Method: get_badges_dict</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_metadata.py#L27'>Method: get_classifiers</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_markdown.py#L290'>Method: get_contributions_markdown</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_relations.py#L26'>Method: get_dependants</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_relations.py#L7'>Method: get_dependencies</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_markdown.py#L89'>Method: get_description_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_markdown.py#L264'>Method: get_examples_markdown</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_markdown.py#L236'>Method: get_footnote_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_markdown.py#L93'>Method: get_information_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_markdown.py#L137'>Method: get_installation_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_pypi.py#L8'>Method: get_latest_release</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_markdown.py#L303'>Method: get_mermaid_markdown</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L101'>Method: get_new_packager</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_relations.py#L37'>Method: get_ordered_packagers</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_markdown.py#L314'>Method: get_org_description_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_relations.py#L59'>Method: get_owners_package_names</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_markdown.py#L67'>Method: get_todos</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_markdown.py#L77'>Method: get_todos_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_metadata.py#L16'>Method: get_topics</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_relations.py#L79'>Method: get_untested_objInfo_dict</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_api.py#L81'>Property: github</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_api.py#L47'>Method: github_available</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_markdown.py#L180'>Method: github_link</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_markdown.py#L189'>Method: github_link_path_line</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_workflow.py#L223'>Method: if_publish_bump</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_workflow.py#L230'>Method: if_publish_publish</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_metadata.py#L33'>Method: is_bumped</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_target.py#L23'>Method: is_django</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_target.py#L27'>Method: is_exe</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/shared.py#L15'>Method: is_general</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_target.py#L19'>Method: is_node</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo_target.py#L15'>Method: is_python</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_api.py#L88'>Property: localmodule</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_api.py#L52'>Method: localmodule_available</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_api.py#L71'>Property: localrepo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_api.py#L42'>Method: localrepo_available</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/shared.py#L11'>Method: name_is_general</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager.py#L56'>Method: new_clean_environment</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager.py#L45'>Method: packagers_from_packages</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_api.py#L95'>Property: pypi</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_api.py#L60'>Method: pypi_available</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L135'>Method: relative_path_is_aesthetic</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_pypi.py#L23'>Method: reserve_name</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_workflow.py#L177'>Method: run_ordered_methods</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_files.py#L284'>Method: set_collapsible</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/shared.py#L20'>Property: simple_name</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager.py#L72'>Method: summary_packagers</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_github.py#L13'>Method: sync_github_metadata</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_metadata.py#L47'>Property: target</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_workflow.py#L218'>Method: upload_package_summary</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_workflow.py#L193'>Method: workflow_sync</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager_workflow.py#L184'>Method: workflow_unittest</a>
└─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/pypi.py#L26'>Class: PyPI</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/github.py#L12'>Class: GitHub</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localmodule.py#L8'>Class: LocalModule</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/localrepo/base/localrepo.py#L15'>Class: LocalRepo</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/packager.py#L17'>Class: Packager</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/pypi.py#L26'>Class: PyPI</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/pypi.py#L47'>Method: download</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/pypi.py#L37'>Method: exists</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/pypi.py#L70'>Method: get_date</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/pypi.py#L59'>Method: get_owners_packages</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/pypi.py#L41'>Method: get_tarball_url</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/pypi.py#L63'>Method: get_version</a>
   └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/c33158d/generalpackager/api/pypi.py#L34'>Property: url</a>
</pre>
</details>


<details open>
<summary><h2>Contributions</h2></summary>

Issue-creation and discussions are most welcome!

Pull requests are not wanted, please discuss with me before investing any time
</details>


<details>
<summary><h2>Todo</h2></summary>

| Module                                                                                                                                                      | Message                                                                                                                                                                                                          |
|:------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_github.py#L1'>packager_github.py</a>                        | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_github.py#L32'>commit-hook failed for auto commit "not a valid Win32 application</a>                             |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_github.py#L1'>packager_github.py</a>                        | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_github.py#L41'>Fetch commit sha locally before pushing, possibly generate sha before commit.</a>                 |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_github.py#L1'>packager_github.py</a>                        | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_github.py#L79'>Setup env vars for project.</a>                                                                   |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_markdown.py#L1'>packager_markdown.py</a>                    | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_markdown.py#L74'>Sort todos by name to decrease automatic commit changes.</a>                                    |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_workflow.py#L1'>packager_workflow.py</a>                    | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_workflow.py#L195'>Add single job to make sure workflow is up to date.</a>                                        |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L1'>pypi.py</a>                                          | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L12'>Move download to it's own package.</a>                                                                   |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L1'>pypi.py</a>                                          | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L66'>Find a faster fetch for latest PyPI version and datetime.</a>                                            |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/github.py#L1'>github.py</a>                                      | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/github.py#L14'>Get and Set GitHub repo private.</a>                                                                   |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/python/localrepo_python.py#L1'>localrepo_python.py</a> | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/python/localrepo_python.py#L64'>Make sure twine is installed when trying to upload to pypi.</a>             |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/python/localrepo_python.py#L1'>localrepo_python.py</a> | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/python/localrepo_python.py#L65'>Look into private PyPI server where we could also do dry runs for test.</a> |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/python/metadata_python.py#L1'>metadata_python.py</a>   | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/python/metadata_python.py#L4'>Dynamic values in DataClass to remove LocalRepos and Metadatas.</a>           |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L1'>localrepo.py</a>                 | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/localrepo/base/localrepo.py#L20'>Search for imports to list dependencies.</a>                                         |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/other/packages.py#L1'>packages.py</a>                                | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/other/packages.py#L11'>Generate Python file in generalpackager containing general packages.</a>                           |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_files.py#L1'>packager_files.py</a>                          | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_files.py#L44'>Watermark generated files to prevent mistake of thinking you can modify them directly.</a>         |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_files.py#L1'>packager_files.py</a>                          | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_files.py#L102'>Generalize get_new_packager which calls recycle_clear on all attributes.</a>                      |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_files.py#L1'>packager_files.py</a>                          | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_files.py#L115'>Fix create_blank, it overwrites current projects pip install.</a>                                 |
</details>


<sup>
Generated 2022-10-19 16:24 CEST for commit <a href='https://github.com/ManderaGeneral/generalpackager/commit/c33158d'>c33158d</a>.
</sup>
</details>

