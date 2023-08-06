import itertools


def first_lower(s):
	return s[0].lower() + s[1:]


def go_args(lst, left='', right=''):
	if not lst: return ''
	return left + ', '.join(f'{x["name"]} {x["Type"]}' for x in lst) + right


def go_args_plural(lst):
	return ', '.join(f'{x["names"]} []{x["Type"]}' for x in lst)


def go_vars(lst, left='', right=''):
	if not lst: return ''
	return left + ', '.join(x["name"] for x in lst) + right


def go_vars_plural(lst):
	return ', '.join(x["names"] for x in lst)


def go_types(lst):
	return ', '.join(x["Type"] for x in lst)


def go_types_plural(lst):
	return ', '.join("[]%s" % x["Type"] for x in lst)


# def go_param_name(s):
#   return first_lower(s)
#
#
# def short_name(s):
#   return ''.join(re.findall('[A-Z]', s)).lower()
mappings = {}
aliases = {}


def gql_fmt(f, s):
	if "$1" in f:
		return f.replace("$1", s)
	return f'{f}({s})'


def gql(s, x, schema):
	return conv(s, x, 'gql', schema)


def spanner(s, x, schema):
	return conv(s, x, 'spanner', schema)


go_primitives = {'bool', 'int', 'int64', 'string'}
gql_primitives = {'datetime'}


def conv(s, obj, t, schema):
	a, b = ab = obj['Type'], obj[t]['Type']
	x, y = "/" + obj['key'], "/" + obj[t]['key']
	items = itertools.product([a + x, a, x], [b + y, b, y])
	if a and a == b:
		if a in go_primitives:
			return s
	for y in list(items) + [ab]:
		if mappings.get(y):
			return gql_fmt(mappings[y], s)
	bs = b.lstrip('*')
	if bs in schema[t] and bs not in gql_primitives and t == 'gql':
		return s + '.ToGraphql()'
	return s


def alias(s, opts=0):
	return aliases.get(s, [s] if opts == 1 else [])


dart_type_mappings = {
	'string': 'String',
	'bool': 'bool',
	'int': 'int',
}

dart_unknown_types = []


# def dart_type(s, x):
#   a = x['gql']['Type']
#   return f'{dart_type_mappings.get(a,s)} {s}'

def dart_optional_type_get(s, x):
	s = s.replace('*', '').replace("[]", "")
	if s not in dart_type_mappings:
		print('unknown type', s)
		dart_unknown_types.append(s)
	s = dart_type_mappings.get(s, s)
	ret = f'List<{s}>' if x['isArray'] else s
	ret = f'required {ret}' if x['notNull'] else f'{ret}?'
	return ret


def dart_args(lst):
	return '\n'.join(f'{dart_optional_type_get(x["Type"], x)} {x["nameExact"]},' for x in lst)


def nothing(s):
	return s


def unknown_types(lst):
	return [x for x in lst if x.get('Type', '').replace('*', '').replace("[]", "") not in dart_type_mappings]


def basename(name):
	return name.split('/')[-1]


def apply_filters(env, m, a):
	env.filters['arg'] = go_args
	env.filters['args'] = go_args_plural
	env.filters['var'] = go_vars
	env.filters['vars'] = go_vars_plural
	env.filters['type'] = go_types
	env.filters['types'] = go_types_plural
	# env.filters['paramname'] = go_param_name
	# env.filters['shortname'] = short_name
	env.filters['gql'] = gql
	env.filters['spanner'] = spanner
	# env.filters['nothing'] = nothing
	env.filters['dart_args'] = dart_args
	env.filters['first_lower'] = first_lower
	env.filters['basename'] = basename
	env.filters['alias'] = alias
	# env.filters['unknown_types'] = unknown_types
	# env.filters['dart_type'] = dart_type
	mappings.update(m)
	aliases.update(a)
