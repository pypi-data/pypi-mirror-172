class ABFException(Exception):
    pass


class ABFBundleNotFoundException(ABFException):
    pass


class ABFBundleVersionNotFoundException(ABFBundleNotFoundException):
    pass


class ABFGitFoundException(ABFException):
    pass


class ABFGitRefNotFoundException(ABFException):
    pass


class ABFBadBundle(ABFException):
    pass


class ABFMissingAction(ABFException):
    pass
