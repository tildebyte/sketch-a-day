htmltext = '''<!DOCTYPE html>
<html>

    <head>
        <link rel="stylesheet" type="text/css" href="sketch-a-day.css">
    </head>

    <body>
        <div class="wrapper">
            <div class="title-box">Sketch-a-Day</div>
            <div class="text-box">
                <p>Prompt for <span class="highlight-date">{0}</span></p>
                <p><span>{1}</span> using <span>{2}</span></p>
            </div>
            <div><a href="https://github.com/tildebyte/sketch-a-day" target="_blank">Source on GitHub</a></div>
            <div id="gh-icon">
                <a href="https://github.com/tildebyte/sketch-a-day" target="_blank"></a>
            </div>
        </div>
        <p>Sketch and Drawing tutorials</p>
        <div class="gallery">
            {3}
        </div>
        <p>Previous prompts</p>
        <div class="history">
            {4}
        </div>
    </body>

</html>
'''
