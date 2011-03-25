<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
<title>{{ title or '' }}</title>
<script src='/static/js/jquery-1.4.2.min.js'></script>
<script src='/static/js/jquery-ui.min.js'></script>
% locals().get('jsblock', lambda: None)()
<link rel="stylesheet" href="/static/css/base.css" type="text/css" media="all" />
<link rel="stylesheet" href="/static/css/jquery-ui.css" type="text/css" media="all" />
% locals().get('cssblock', lambda: None)()
</head>

<body>
<div style='text-align: right;'>
	% if locals().get('loggedin_user', None):
		Logged in as <a href='#'>{{ loggedin_user.username }}</a>
	% else:
		<a href='#'>login</a>
	% end
</div>
%include
</body>

</html>
