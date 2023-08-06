
# verser

    from verser import Project, get_next_version

Version tracker for your python package

### next version
    project = Project(package_name="my_cool_package", default_version="0.0.0.0")

    next_version = get_next_version(
        project=project,
        increment_=True,
        pre_release=False,
        verbose=True
    )  
    print(next_version)
    # 0.0.0.1

### pre release 
    project = Project(package_name="my_cool_package", default_version="0.0.0.0")

    next_version = get_next_version(
        project=project,
        increment_=True,
        pre_release=True ,
        verbose=True
    )  
    print(next_version)
    # 0.0.0.1rc1

### creates __version__.py file with your new version
    project = Project(package_name="my_cool_package", default_version="0.0.0.0")

    next_version = get_next_version(
        project=project,
        increment_=True,
        pre_release=True ,
        verbose=True
    )  
    print(next_version)
    # 0.0.0.1rc1