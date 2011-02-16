<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
<title>{{ title or '' }}</title>
<script src='https://ajax.googleapis.com/ajax/libs/jquery/1.5.0/jquery.min.js' type='text/javascript'></script>
% locals().get('jsblock', lambda: None)()
</head>

<body>
<div style='text-align: right;'>
	% if loggedin_user:
		Logged in as <a href='#'>{{ loggedin_user.username }}</a>
	% else:
		<a href='#'>login</a>
</div>
%include
</body>

</html>
