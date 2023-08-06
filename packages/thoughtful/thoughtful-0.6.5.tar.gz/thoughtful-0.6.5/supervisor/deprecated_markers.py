from __future__ import annotations

import warnings

DOCUMENTATION_URL = "https://www.notion.so/4498bd02de8f41858f6cb44a04b96fd9"


def deprecate_non_dynamic(stacklevel: int = 2):
    warnings.simplefilter("once", DeprecationWarning)
    warnings.warn(
        f"This function uses the old supervisor non-dynamic pattern and will be removed soon. For more information, see: {DOCUMENTATION_URL}",
        DeprecationWarning,
        stacklevel=stacklevel,
    )


class DeprecatedBecauseNonDynamic:
    def __init_subclass__(cls, **kwargs):
        warnings.simplefilter("once", DeprecationWarning)
        warnings.warn(
            f"This class uses the old supervisor non-dynamic pattern and will be removed soon. For more information, see: {DOCUMENTATION_URL}",
            DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)

        super().__init_subclass__(**kwargs)
