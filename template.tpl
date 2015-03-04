<html>
    <head>
        <title>{{ title }}</title>
    </head>
    <body>
        <h1>{{ title }}</h1>
        <p>{{ desc or "Sorry, no description is available for this file." }}</p>
        <p>You can download the file <a href={{ title }}.pdf>here</a>.</p>
        <img src="cover.jpg">
    </body>
</html>
