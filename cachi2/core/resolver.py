from collections.abc import Iterable
from typing import Callable

from cachi2.core.errors import UnsupportedFeature
from cachi2.core.models.input import PackageManagerType, Request
from cachi2.core.models.output import RequestOutput
from cachi2.core.package_managers import gomod

Handler = Callable[[Request], RequestOutput]

_package_managers: dict[PackageManagerType, Handler] = {
    "gomod": gomod.fetch_gomod_source,
}


supported_package_managers = list(_package_managers)


def resolve_packages(request: Request) -> RequestOutput:
    """Run all requested package managers, return their combined output."""
    requested_types = set(pkg.type for pkg in request.packages)
    unsupported_types = requested_types - _package_managers.keys()
    if unsupported_types:
        raise UnsupportedFeature(
            f"Package manager(s) not yet supported: {', '.join(sorted(unsupported_types))}",
            # unknown package managers shouldn't get past input validation
            solution="But the good news is that we're already working on it!",
        )
    pkg_managers = [_package_managers[type_] for type_ in sorted(requested_types)]
    return _merge_outputs(pkg_manager(request) for pkg_manager in pkg_managers)


def _merge_outputs(outputs: Iterable[RequestOutput]) -> RequestOutput:
    """Merge RequestOutput instances."""
    packages = []
    env_vars = []
    for output in outputs:
        packages.extend(output.packages)
        env_vars.extend(output.environment_variables)
    return RequestOutput(packages=packages, environment_variables=env_vars)
