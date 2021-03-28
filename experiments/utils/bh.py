def benjaminiHochberg(pvals, globalAlpha):
    from numpy import argsort, array
    """Returns list indicating which p-values are significant after benjamini hochberg correction.
    This is also known as Holm-Bonferroni method

    Args:
        pvals ([float]): Array of all p-values
        globalAlpha (float): The global alpha ot be used.
    """
    mapOrdered = argsort(array(pvals))
    for idx, p in enumerate(mapOrdered):
        pvals[p] = pvals[p] < globalAlpha/(len(pvals)-idx)
        if pvals[p]==0:
            for j in range(idx, len(pvals)):
                pvals[mapOrdered[j]] = False
            break
    return pvals