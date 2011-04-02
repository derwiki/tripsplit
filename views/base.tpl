<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xmlns:fb="http://www.facebook.com/2008/fbml">
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
    <div id="fb-root"></div>
    <script src="http://connect.facebook.net/en_US/all.js"></script>
    <script>
       FB.init({ appId:'214571255223379', cookie:true, status:true, xfbml:true });
    </script>
    <fb:login-button>Login with Facebook</fb:login-button>
</div>
%include
</body>

</html>
