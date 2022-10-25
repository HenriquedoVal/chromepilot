def get_newer_version(versions: list[str]) -> str:
    versions.sort(
        key=lambda x: (x.split('.')[0],
                       x.split('.')[2],
                       x.split('.')[3]),
        reverse=True
    )

    if len(versions) > 0:
        return versions[0]


def is_x_newer_than_y(x: str, y: str) -> bool:
    if y is None:
        return True

    x = [int(i) for i in x.split('.')]
    y = [int(i) for i in y.split('.')]
    for ind in (0, 2, 3):
        if x[ind] > y[ind]:
            return True
    return False
