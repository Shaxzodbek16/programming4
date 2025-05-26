EMAIL_TEMPLATE_FOR_CODE = """<!DOCTYPE html>
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

EMAIL_TEMPLATE_FOR_WARNINGS = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Low Stock Alert</title>
  <style>
    /* Reset */
    body, table, td, p { margin:0; padding:0; }
    img { border:0; display:block; }

    /* Base */
    body { background-color: #f9f9f9; font-family: Arial, sans-serif; }
    .wrapper { width:100%; table-layout: fixed; background-color: #f9f9f9; padding: 20px 0; }
    .container { max-width:600px; margin:0 auto; background-color:#ffffff; border-radius:8px; overflow:hidden; }
    .header { background-color: #d9534f; color:#ffffff; text-align:center; padding:25px; }
    .header h2 { font-size:20px; margin:0; }
    .content { padding:30px; color:#444444; font-size:16px; line-height:1.6; }
    .button { display:inline-block; padding:10px 20px; background-color:#d9534f; color:#ffffff; text-decoration:none; border-radius:4px; margin-top:20px; }
    .footer { background-color:#f1f1f1; color:#777777; font-size:12px; text-align:center; padding:15px 30px; }
    .footer a { color:#d9534f; text-decoration:none; }

    /* Responsive */
    @media only screen and (max-width: 600px) {
      .header, .content, .footer { padding:20px !important; }
      .content { font-size:14px !important; }
    }
  </style>
</head>
<body>
  <table class="wrapper" role="presentation" width="100%">
    <tr>
      <td align="center">
        <table class="container" role="presentation" width="100%">
          <tr>
            <td class="header">
              <h2>⚠️ Low Stock Alert</h2>
            </td>
          </tr>
          <tr>
            <td class="content">
              <p>Hello,</p>
              <p>The product <strong>{{PRODUCT_NAME}}</strong> is running low in our warehouse stock.</p>
              <p>Please restock it as soon as possible to avoid any interruptions.</p>
              <a href="https://shaxzodbek.com" class="button">View Inventory</a>
            </td>
          </tr>
          <tr>
            <td class="footer">
              <p>This is an automated message—please do not reply.</p>
              <p>Questions? Contact us at <a href="mailto:muxtorovshaxzodbek16@gmail.com">muxtorovshaxzodbek16@gmail.com</a>.</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""
