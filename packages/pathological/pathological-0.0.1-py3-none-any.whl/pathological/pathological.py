"""
Pathological - a module to work with the file system in an object-oriented manner
"""
from typing import Optional, Literal, Generator
import os
import sys

## module-level members
this: object = sys.modules[__name__]
this.nt_sep: str = '\\'
this.posix_sep: str = '/'
this.path_seps: dict[str, str] = {'nt': this.nt_sep, 'posix': this.posix_sep}


def os_type_is_valid_type(os_type: Optional[str]) -> bool:
    """Returns boolean indicating whether specified OS Type is valid (according to this.path_seps.keys())"""
    if os_type is None:
        return False
    return os_type in this.path_seps.keys()


def handle_os_type_arg(func: callable) -> object:
    """Decorator/wrapper function for handling os_type arguments in function calls"""
    def check_os_type(*args: list, **kwargs: dict) -> object:
        ## check if os_type is a parameter
        os_type_key: str = 'os_type'
        if os_type_key in kwargs.keys():
            os_type_specified: str = kwargs[os_type_key].lower()
            os_type: str
            ## if os_type argument is valid os_type, exit inner function
            if os_type_specified in this.path_seps.keys():
                return func(*args, **kwargs)
            ## if os_type is infer, set os_type equal to results of infer_os_type
            elif os_type_specified == 'infer':
                ## if infer, path must be specified
                path: str
                ## attempt to get path from specified keyword list, else get first arg from args
                if 'path' in kwargs.keys():
                    path = kwargs['path']
                else:
                    path = args[0]
                os_type = infer_os_type(path)
            ## os_type is invalid or 'sys', set os_type equal to os.name
            else:
                os_type = os.name
            ## edit kwargs to use modified os_type
            kwargs[os_type_key] = os_type
        ## call original function with updated args and kwargs
        return func(*args, **kwargs)
    return check_os_type


def path_contains_windows_drive_letter(path: str) -> bool:
    """Evaluates a path and returns a boolean indicating whether or not path appears to contain a valid Windows drive"""
    ## base condition - ensure path contains at least two characters
    if len(path) < 2:
        return False
    ## return True if path starts with alpha character followed by a colon else False
    return path[0].isalpha() and path[1] == ':'


def path_is_unc(path: str) -> bool:
    """Evaluate a path and return a boolean indicating whether or not path appears to be a 'Universal Naming Convention' path"""
    ## evaluate path using nt and posix evaluators
    return path_is_nt_unc(path) or path_is_posix_unc(path)


def path_is_nt_unc(path: str) -> bool:
    """Evaluate a path and return a boolean indicating whether or not a path appears to be a NT 'Universal Naming Convention' path"""
    ## base condition - if path is less than two characters, return False
    if len(path) < 2:
        return False
    ## if first two characters of path indicate 2 nt style separators, return True, else False
    return path[:2] == '\\\\'


def path_is_posix_unc(path: str) -> bool:
    """Evaluate a path and return a boolean indicating whether or not a path appears to be a Posix 'Universal Naming Convention' path"""
    ## base condition - if path is less than two characters, return False
    if len(path) < 2:
        return False
    ## if first two characters of path indicate 2 Posix style separators, return True, else False
    return path[:2] == '//'


@handle_os_type_arg
def split_path(path: str, os_type: Literal['posix','nt','infer'] = 'infer') -> list[str]:
    """Splits a path on a separator based on the specified OS type and returns list of path components"""
    return posixpath_split(path) if os_type == 'nt' else ntpath_split(path)


def posix_split(path: str, all: bool = False, split_ext: bool = False) -> list[str]:
    """"""
    return_list: list[str]
    if not all:
        return_list = posixpath.split(this.path_seps['posix'])
        
    if not all and not split_ext:
        return components[-1:]
    if all and not split_ext:
        return components
    return components


@handle_os_type_arg
def join_path(*path_components: tuple, os_type: Literal['posix','nt','infer'] = 'infer') -> str:
    """Splits a path on a separator based on the specified OS type and returns list of path components"""
    return ntpath.join(*path_components) if os_type == 'nt' else posixpath.join(*path_components)


@handle_os_type_arg
def convert_path_sep(path: str,
                     os_type: Literal['posix','nt','sys','infer'] = 'infer') -> str:
        """
        Convert a path to either Unix or Windows -style path

        Args:
            path(str): path that contains separators to be converted
            os_type([Literal['posix','nt','infer']): defaults to 'infer'; all path separators will be converted to the type of the specified os_type

        Returns:
            str: path with separators for the specified operating system
        """
        ## handle sys and infer args:
        if os_type not in this.path_seps.keys():
            return convert_path_sep(path=path, os_type=os_type)
        ## determine change_to separator based on os_type
        change_to: str = this.path_seps[os_type]
        ## determine change_from separator based on remaining key in path_seps dict
        change_from: str = this.path_seps[list(set(this.path_seps.keys()) - {os_type})[0]]
        ## return path with path converted to target os_type
        return path.replace(change_from, change_to)


@handle_os_type_arg
def infer_os_type(path: str,
                  path_split_weight: Optional[int] = 1,
                  windows_drive_letter_weight: Optional[int] = 1) -> str:
    """
    Determine os type (Posix/NT) characteristics of provided file path:

    Abstract
      - Evaluates path and assigns point to either NT or Posix dependent on outcome 
        of each evaluation
      - In case of tie, adds points to os type that matches host os (os.name)
      - Returns OS type with most points 

    Args:
        path(str): string representing a Path to be analyzed
        ##os_name_weight(int): amount of weight is given to os.name attribute from os module
        ##path_split_score_min_weight: amount of weight given to path split scores when results are close
        ##path_split_score_max_weight: amount of weight given to path split scores when results are not close

    Returns:
        str: string literal of inferred OS Type ('posix' or 'nt')
    """
    ## one-liner helper functions
    def get_key_with_max_value(dictionary: dict) -> str:
        return max(dictionary, key=dictionary.get)

    def get_key_with_min_value(dictionary: dict) -> str:
        return min(dictionary, key=dictionary.get)

    def get_max_value(dictionary: dict) -> int:
        return max(dictionary.values())

    def get_min_value(dictionary: dict) -> int:
        return min(dictionary.values())

    def all_values_equal(dictionary: dict) -> bool:
        first_value: object = list(dictionary.values())[0]
        value: object
        for value in dictionary.values():
            if value != first_value:
                return False
        return True

    ## create empty dictionary to store scores
    os_type_scores: dict = {}
    ## get dictionary of os types and corresponding counts from splitting path on 
    ##   corresponding path separators
    ## get count of items returned by splitting on each separator
    os_type_counts: dict = {os_type: len(path.split(sep)) for os_type, sep in this.path_seps.items()}
    ## get min/max counts from os_type_counts
    os_type_count_max: int = get_max_value(os_type_counts)
    os_type_count_min: int = get_min_value(os_type_counts)
    ## if more than one item is returned from greater split and nothing is split from other, give twice as much weight to this
    ## iterate over os_types and calculate scores, storing results in os_type_scores dict
    for os_type in this.path_seps.keys():
        os_type_scores[os_type] = 0
        ## add points if the os_type_count score is more than the other
        os_type_scores[os_type] += path_split_weight * (os_type_counts[os_type] == os_type_count_max)
        ## add points if windows drive letter is identified
        os_type_scores[os_type] += windows_drive_letter_weight * (path_contains_windows_drive_letter(path) and os_type=='nt')
    ## determine os_type based on scores
    ## os.name match is worth 2 points
    ## path_split score is worth 1 unless split difference heavily leans towards one side, else 2 points
    ## if tie, add points for os.name
    if all_values_equal(os_type_scores):
        return os.name
    os_type = get_key_with_max_value(os_type_scores)
    return os_type


@handle_os_type_arg
def get_child_items(path: str,
                    recursive: Optional[bool] = True,
                    exclude: Optional[Literal['files','file','directories','dir']] = None,
                    include: Optional[Literal['files','file','directories','dir']] = None,
                    exclude_extensions: Optional[list[str] | str] = None,
                    include_extensions: Optional[list[str] | str] = None,
                    path_type: Optional[Literal['absolute','abs','relative',
                                                'rel','extensions','ext']] = 'absolute',
                    os_type: Optional[Literal['nt','posix','infer']] = 'infer') -> Generator[str, None, None]:
    """
    Generator that yields child items in a provided directory and any subdirectories, if specified; similar to Powershell's Get-ChildItem commandlet

    Args:
        path(str): starting path
        recursive(Optional[bool]): defaults to True; indicates whether to recursively list file extensions found in any sub-directories
        unique(Optional[bool]): defaults to True; when True, ensures each file extension is only returned a single time
        exclude(Optional[Literal['files','directories']]): when provided, objects of the specified type will be discarded
        include(Optional[Literal['files','directories']]): when provided, object not of the specified type will be discarded
        exclude_extensions(List[str] | str): when provided, files with these extensions will be discarded
        include_extensions(List[str] | str): when provided, files without these extensions these will be discarded
        path_type(str): defaults to 'absolute'; indicates whether to return 'absolute' filepaths, 'relative' filepaths, or file 'extensions' only
        os_type(str): defaults to 'sys' which equates to os.name; all filepaths will have path separators for the specified os_type

    Yields:
        a string representing a path to an object in the file system
    """
    ## base case - nothing in path, return None
    if len(os.listdir(path)) == 0:
        return None
    ## iterate over objects in specified directory
    _ : str
    for _ in os.listdir(path):
        ## get absolute path
        ap_: str = os.path.join(path, _)
        ## convert path based on specified type
        ap_ = convert_path_sep(ap_, os_type)
        if path_type == 'absolute':
            ## add absolute path to filename to ensure valid path is passed to isfile/isdir functions
            ## convert to posixpath
            #_ = assert_path_sep(ap_, os_type)
            _ = ap_

        ## handle file extension arguments
        #if exclude_extensions is not None or include_extensions is not None:
        ## strip decimals from both sides of comparison to be as greedy as possible
        ext: str = os.path.splitext(ap_)[1].lower().strip('.')
        temp_val: str
        ## if exlcude_extensions is provided, then ensure file in question isn't blacklisted
        if exclude_extensions:
            ## handle str argument
            #print(f"ext: {ext} ; exclude_extensions: {exclude_extensions}")
            exclude_extensions = [exclude_extensions] if not isinstance(exclude_extensions, list) else exclude_extensions
            exclude_extensions = [temp_val.lower().strip('.') for temp_val in exclude_extensions]
            if ext in exclude_extensions:
                continue
        ## if include_extensions is provided, then ensure file in question is whitelisted
        if include_extensions:
            #print(f"ext: {ext} ; include_extensions: {include_extensions}")
            ## handle str argument
            include_extensions = [include_extensions] if not isinstance(include_extensions, list) else include_extensions
            include_extensions = [temp_val.lower().strip('.') for temp_val in include_extensions]
            if ext not in include_extensions and os.path.isfile(ap_):
                continue
        ## if user specifies extensions only, then set return val to file extension of file
        if os.path.isfile(ap_) and path_type.lower() in {'extensions', 'ext'}:
            _ = os.path.splitext(ap_)[1]
            yield _
            continue
        ## if object is file, only return if specified
        if os.path.isfile(ap_) and \
        exclude not in {'files','file'} and \
        include not in {'directories','dir','extensions','ext'}:
            yield _
            continue
        ## if object is directory, only return if specified
        elif os.path.isdir(ap_) and \
        exclude not in {'directories','dir'} and \
        include not in {'files','file','extensions','ext'} \
        and path_type not in {'extensions','ext'}:
            yield _
        ## if item is directory and recursive is specified, call 
        ## get_child_items using current item as directory argument
        if os.path.isdir(ap_) and recursive:
            yield from get_child_items(path=ap_,recursive=recursive,include=include,exclude=exclude,
                                       include_extensions=include_extensions,
                                       exclude_extensions=exclude_extensions,
                                       path_type=path_type,os_type=os_type)


@handle_os_type_arg
def list_directories(path: str,
                     recursive: Optional[bool] = True,
                     unique: bool = True,
                     path_type: Optional[Literal['absolute','abs','relative',
                                        'rel','extensions','ext']] = 'absolute',
                     os_type: Optional[Literal['nt','posix','sys']] = 'sys') -> list[str]:
    """
    Returns list of all directories and subdirectories, if specified, in a given directory

    Args:
        path(str): starting path
        recursive(Optional[bool]): defaults to True; indicates whether to recursively list file extensions found in any sub-directories
        unique(Optional[bool]): defaults to True; when True, ensures each file extension is only returned a single time
        path_type(str): defaults to 'absolute'; indicates whether to return 'absolute' filepaths, 'relative' filepaths, or file 'extensions' only
        os_type(str): defaults to 'sys' which equates to os.name; all filepaths will have path separators for the specified os_type    

    Returns:
        list[str]: List of strings representing file paths to directories found in the file system under the specified directory
    """
    ## get generator from get_child_items for directories only
    gen: Generator[str, None, None] = get_child_items(path=path, recursive=recursive, 
                                                      exclude=None, include='directories', 
                                                      exclude_extensions=None, 
                                                      include_extensions=None, 
                                                      path_type=path_type, os_type=os_type)
    _ : str
    directories: list[str] = [_ for _ in gen]
    ## if only uniques are desired, then reduce list to uniques only, else return full list
    if unique:
        return list(set(directories))
    return directories


@handle_os_type_arg
def list_files(path: str, 
               recursive: Optional[bool] = True, 
               unique: bool = True, 
               path_type: Optional[Literal['absolute','abs','relative',
                                           'rel','extensions','ext']] = 'absolute',
               exclude_extensions: Optional[list[str] | str] = None,
               include_extensions: Optional[list[str] | str] = None,
               os_type: Optional[Literal['nt','posix','sys']] = 'sys') -> list[str]:
    """
    Returns list of all files in a given directory and any subdirectories, if specified

    Args:
        path(str): starting path
        recursive(Optional[bool]): defaults to True; indicates whether to recursively list file extensions found in any sub-directories
        unique(Optional[bool]): defaults to True; when True, ensures each file extension is only returned a single time
        path_type(str): defaults to 'absolute'; indicates whether to return 'absolute' filepaths, 'relative' filepaths, or file 'extensions' only
        exclude_extensions(List[str] | str): when provided, files with these extensions will be discarded
        include_extensions(List[str] | str): when provided, files without these extensions these will be discarded
        os_type(str): defaults to 'sys' which equates to os.name; all filepaths will have path separators for the specified os_type    

    Returns:
        list[str]: List of strings representing file paths to files found in the file system under the specified directory
    """
    ## get generator from get_child_items for files only
    gen: Generator[str, None, None] = get_child_items(path=path, recursive=recursive, 
                                                      exclude=None, include='files', 
                                                      exclude_extensions=exclude_extensions, 
                                                      include_extensions=include_extensions, 
                                                      path_type=path_type, os_type=os_type)
    _ : str
    files: list[str] = [_ for _ in gen]
    ## if only uniques are desired, then reduce list to uniques only, else return full list
    if unique:
        return list(set(files))
    return files


@handle_os_type_arg
def list_file_extensions(path: str,
                         recursive: Optional[bool] = True,
                         unique: bool = True,
                         exclude_extensions: Optional[list[str] | str] = None,
                         include_extensions: Optional[list[str] | str] = None,
                         os_type: Optional[Literal['nt','posix','sys']] = 'sys') -> list[str]:
    """
    Returns list of file extensions found in directory and subdirectories, if specified

    Args:
        path(str): starting path
        recursive(Optional[bool]): defaults to True; indicates whether to recursively list file extensions found in any sub-directories
        unique(Optional[bool]): defaults to True; when True, ensures each file extension is only returned a single time
        exclude_extensions(List[str] | str): when provided, files with these extensions will be discarded
        include_extensions(List[str] | str): when provided, files without these extensions these will be discarded
        os_type(str): defaults to 'sys' which equates to os.name; all filepaths will have path separators for the specified os_type

    Returns:
        list[str]: List of strings representing file extensions of files found in the file system under the specified directory
    """
    ## get generator from get_child_items for file extensions only
    gen: Generator[str, None, None] = get_child_items(path=path, recursive=recursive, 
                                                      exclude=None, include=None, 
                                                      exclude_extensions=exclude_extensions, 
                                                      include_extensions=include_extensions, 
                                                      path_type='extensions', os_type=os_type)
    _ : str
    extensions: list[str] = [_ for _ in gen]
    ## if only uniques are desired, then reduce list to uniques only, else return full list
    if unique:
        return list(set(extensions))
    return extensions