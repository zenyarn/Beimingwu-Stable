import zipfile
import os
import shutil


def get_top_folder_in_zip(zfile: zipfile.ZipFile):
    """
    Get the top folder in a zip file.
    """
    top_folders = set()
    for name in zfile.namelist():
        if name.endswith("/"):
            # it is a folder
            name = name[:-1]
            if "/" not in name:
                # it is a top folder
                top_folders.add(name)
                pass
            pass
        else:
            if "/" not in name:
                # it is a top file
                return ""
            pass
        pass

    if len(top_folders) == 1:
        return top_folders.pop() + "/"
    else:
        return ""
    pass


def delete_folder_content(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
            pass
        pass
    pass


def search_sensitive_words(text, sensitive_pattern):
    """
    Search sensitive words in text.
    """
    stopwords = set(
        [
            "!",
            '"',
            "#",
            "$",
            "%",
            "&",
            "'",
            "(",
            ")",
            "*",
            "+",
            ",",
            "-",
            ".",
            "/",
            ":",
            ";",
            "<",
            "=",
            ">",
            ">>",
            "?",
            "@",
            "[",
            "\\",
            "]",
            "^",
            "}",
            "~",
        ]
    )

    if sensitive_pattern is None:
        return []

    for ch in stopwords:
        text = text.replace(ch, " ")
        pass

    ret = []
    for m in sensitive_pattern.finditer(text):
        ret.append(m.group(0).strip())
        pass

    return ret
