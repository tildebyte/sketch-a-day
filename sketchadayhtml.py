htmltext = '''<!DOCTYPE html>
<html>

    <head>
        <link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family=Fira+Sans:300|Source+Serif+Pro">
        <link rel="stylesheet" type="text/css" href="sketch-a-day.css">
    </head>

    <body>
        <div id="wrapper">
            <div id="title-box">Sketch-a-Day</div>
            <div id="text-box">
                <p class="prompt">Prompt for <span id="highlight-date">{0}</span></p>
                <p class="prompt"><span id="highlight">{1}</span> using <span id="highlight">{2}</span></p>
            </div>
            <div><a id="link" href="https://github.com/tildebyte/sketch-a-day" target="_blank">Source on GitHub</a></div>
            <a href="https://github.com/tildebyte/sketch-a-day target="_blank""><img id="gh-mark" src="GitHub-Mark-32px.png" alt="GitHub logo"></a>
        </div>
        <div id="history">
            {3}
        </div>
    </body>

</html>
'''
