def benjaminiHochberg(pvals, globalAlpha):
    from numpy import argsort, array
    """Returns list indicating which p-values are significant after benjamini hochberg correction.
    This is also known as Holm-Bonferroni method

    Args:
        pvals ([float]): Array of all p-values
        globalAlpha (float): The global alpha ot be used.
    """

    mapOrdered = argsort(array(pvals))
    print(mapOrdered)
    for idx, p in enumerate(mapOrdered):
        print(p, idx, pvals[p], globalAlpha/(len(pvals)-idx))
        pvals[p] = pvals[p] < globalAlpha/(len(pvals)-idx)
        if pvals[p] is False:
            for j in range(idx, len(pvals)):
                pvals[mapOrdered[j]] = False
            break
    return pvals