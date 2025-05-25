EMAIL_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verification Code</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .content {
            padding: 40px 30px;
            text-align: center;
        }
        .code-box {
            background: #f8f9ff;
            border: 2px dashed #667eea;
            border-radius: 8px;
            padding: 25px;
            margin: 25px 0;
        }
        .code {
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
            letter-spacing: 8px;
            font-family: 'Courier New', monospace;
        }
        .message {
            color: #666;
            line-height: 1.6;
            margin: 20px 0;
        }
        .footer {
            background: #f8f8f8;
            padding: 20px;
            text-align: center;
            color: #999;
            font-size: 12px;
        }
        
        .footer p a {
            color: #667eea;
            text-decoration: none;
        }
        .button {
            display: inline-block;
            padding: 12px 25px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 15px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 Verification Code</h1>
        </div>

        <div class="content">
            <p class="message">
                Hello! <br>
                We received a request to verify your email address: <strong>{{EMAIL}}</strong>
            </p>

            <div class="code-box">
                <div class="code">{{CODE}}</div>
            </div>

            <p class="message">
                Enter this code to complete your verification.<br>
                <strong>This code expires in 5 minutes.</strong>
            </p>

            <p class="message">
                If you didn't request this code, please ignore this email.
            </p>
        </div>

        <div class="footer">
            <p>This is an automated message. Please do not reply.</p>
            <p>&copy; 2024 <a href="shaxzodbek.com">Shaxzodbek </a>. All rights reserved.</p>
        </div>
    </div>
</body>
</html>"""
