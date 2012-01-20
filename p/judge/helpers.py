def get_parent_list(namespace):
  result = []
  if namespace != None:
    result.append(namespace)
    while result[-1].parent:
      result.append(namespace.parent)
    result.reverse()
  return result

