def send_wait_list_html_email(name: str) -> str:
    """
    Generates the HTML content for the wait list email.

    Args:
        name (str): The name of the recipient.

    Returns:
        str: The HTML content for the wait list email.
    """
    return f"""<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml"
      xmlns:v="urn:schemas-microsoft-com:vml"
      xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <title></title>
  <!--[if !mso]><!-->
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <!--<![endif]-->
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style type="text/css">
      #outlook a {{
    padding: 0;
      }}

      body {{
    margin: 0;
    padding: 0;
    -webkit-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
      }}

      table,
      td {{
    border-collapse: collapse;
    mso-table-lspace: 0pt;
    mso-table-rspace: 0pt;
      }}

      img {{
    border: 0;
    height: auto;
    line-height: 100%;
    outline: none;
    text-decoration: none;
    -ms-interpolation-mode: bicubic;
      }}

      p {{
    display: block;
    margin: 0;
      }}
  </style>
  <!--[if mso]>
  <noscript>
    <xml>
      <o:OfficeDocumentSettings>
        <o:AllowPNG />
        <o:PixelsPerInch>96</o:PixelsPerInch>
      </o:OfficeDocumentSettings>
    </xml>
  </noscript>
  <![endif]-->
  <!--[if lte mso 11]>
  <style type="text/css">
    .ogf {{
    width: 100% !important;
    }}
  </style>
  <![endif]-->
  <!--[if !mso]><!-->
  <link href="https://fonts.googleapis.com/css?family=Karla:700,400" rel="stylesheet" type="text/css" />
  <style type="text/css"></style>
  <!--<![endif]-->
  <style type="text/css">
      @media only screen and (min-width: 599px) {{
    .xc120 {{
      width: 120px !important;
      max-width: 120px !important;
    }}
    .xc568 {{
      width: 568px !important;
      max-width: 568px !important;
    }}
  }}
  </style>
  <style media="screen and (min-width:599px)">
      .moz-text-html .xc120 {{
    width: 120px !important;
    max-width: 120px;
      }}

      .moz-text-html .xc568 {{
    width: 568px !important;
    max-width: 568px;
      }}
  </style>
  <style type="text/css">
      @media only screen and (max-width: 598px) {{
    table.fwm {{
      width: 100% !important;
    }}
    td.fwm {{
      width: auto !important;
    }}
  }}
  </style>
  <style type="text/css">
      u + .emailify .gs {{
    background: #000;
    mix-blend-mode: screen;
    display: inline-block;
    padding: 0;
    margin: 0;
      }}

      u + .emailify .gd {{
    background: #000;
    mix-blend-mode: difference;
    display: inline-block;
    padding: 0;
    margin: 0;
      }}

      p {{
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
      }}

      a[x-apple-data-detectors] {{
    color: inherit !important;
    text-decoration: none !important;
      }}

      u + .emailify a {{
    color: inherit !important;
    text-decoration: none !important;
      }}

      #MessageViewBody a {{
    color: inherit !important;
    text-decoration: none !important;
      }}

      td.b .klaviyo-image-block {{
    display: inline;
    vertical-align: middle;
      }}

      @media only screen and (max-width: 599px) {{
    .emailify {{
      height: 100% !important;
      margin: 0 !important;
      padding: 0 !important;
      width: 100% !important;
    }}
    u + .emailify.glist {{
      margin-left: 1em !important;
    }}
    td.ico.v > div.il > a.l.m,
    td.ico.v.mn-label {{
      padding-right: 0 !important;
      padding-bottom: 16px !important;
    }}
    td.x {{
      padding-left: 0 !important;
      padding-right: 0 !important;
    }}
    .fwm img {{
      max-width: 100% !important;
      height: auto !important;
    }}
    .aw img {{
      width: auto !important;
      margin-left: auto !important;
      margin-right: auto !important;
    }}
    .awl img {{
      width: auto !important;
      margin-right: auto !important;
    }}
    .awr img {{
      width: auto !important;
      margin-left: auto !important;
    }}
    .ah img {{
      height: auto !important;
    }}
    td.b.nw > table,
    td.b.nw a {{
      width: auto !important;
    }}
    td.stk {{
      border: 0 !important;
    }}
    td.u {{
      height: auto !important;
    }}
    br.sb {{
      display: none !important;
    }}
    .thd-1.i-thumbnail {{
      display: inline-block !important;
      height: auto !important;
      overflow: hidden !important;
    }}
    .hd-1 {{
      display: block !important;
      height: auto !important;
      overflow: visible !important;
    }}
    .ht-1 {{
      display: table !important;
      height: auto !important;
      overflow: visible !important;
    }}
    .hr-1 {{
      display: table-row !important;
      height: auto !important;
      overflow: visible !important;
    }}
    .hc-1 {{
      display: table-cell !important;
      height: auto !important;
      overflow: visible !important;
    }}
    div.r.pr-16 > table > tbody > tr > td,
    div.r.pr-16 > div > table > tbody > tr > td {{
      padding-right: 16px !important;
    }}
    div.r.pl-16 > table > tbody > tr > td,
    div.r.pl-16 > div > table > tbody > tr > td {{
      padding-left: 16px !important;
    }}
      }}

      @media (prefers-color-scheme: light) and (max-width: 599px) {{
    .ds-1 .hd-1 {{
      display: none !important;
      height: 0 !important;
      overflow: hidden !important;
    }}
      }}

      @media (prefers-color-scheme: dark) and (max-width: 599px) {{
    .ds-1 .hd-1 {{
      display: block !important;
      height: auto !important;
      overflow: visible !important;
    }}
      }}
  </style>
  <meta name="color-scheme" content="light dark" />
  <meta name="supported-color-schemes" content="light dark" />
  <!--[if gte mso 9]>
  <style>
    a:link,
    span.MsoHyperlink {{
      mso-style-priority: 99;
      color: inherit;
      text-decoration: none;
    }}

    a:visited,
    span.MsoHyperlinkFollowed {{
      mso-style-priority: 99;
      color: inherit;
      text-decoration: none;
    }}

    li {{
      text-indent: -1em;
    }}

    table,
    td,
    p,
    div,
    span,
    ul,
    ol,
    li,
    a {{
      mso-hyphenate: none;
    }}

    sup,
    sub {{
      font-size: 100% !important;
    }}
  </style>
  <![endif]-->
</head>
<body lang="en" link="#DD0000" vlink="#DD0000" class="emailify"
      style="mso-line-height-rule: exactly; mso-hyphenate: none; word-spacing: normal; background-color: #1e1e1e;">
<div class="bg" style="background-color: #1e1e1e" lang="en">
  <!--[if mso | IE]>
  <table align="center" border="0" cellpadding="0" cellspacing="0"
         class="r-outlook -outlook pr-16-outlook pl-16-outlook -outlook" role="presentation" style="width:600px;"
         width="600">
    <tr>
      <td style="line-height:0;font-size:0;mso-line-height-rule:exactly;">
  <![endif]-->
  <div class="r pr-16 pl-16"
       style="background: #fffffe; background-color: #fffffe; margin: 0px auto; max-width: 600px;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
           style="background: #fffffe; background-color: #fffffe; width: 100%">
      <tbody>
      <tr>
        <td style="border: none; direction: ltr; font-size: 0; padding: 28px 32px 28px 32px; text-align: left;">
          <!--[if mso | IE]>
          <table role="presentation" border="0" cellpadding="0" cellspacing="0">
            <tr>
              <td class="" style="vertical-align:middle;width:120px;">
          <![endif]-->
          <div class="xc120 ogf"
               style="font-size: 0; text-align: left; direction: ltr; display: inline-block; vertical-align: middle; width: 100%;">
            <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
              <tbody>
              <tr>
                <td style="vertical-align: middle; padding: 0 0 0 0">
                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%">
                    <tbody>
                    <tr>
                      <td align="left" class="i"
                          style="font-size: 0; padding: 0; word-break: break-word;">
                        <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                               style="border-collapse: collapse; border-spacing: 0;">
                          <tbody>
                          <tr>
                            <td style="width: 120px">
                              <!-- Logo image can be placed here -->
                            </td>
                          </tr>
                          </tbody>
                        </table>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
          <!--[if mso | IE]>
          </td></tr></table>
          <![endif]-->
        </td>
      </tr>
      </tbody>
    </table>
  </div>
  <!--[if mso | IE]>
  </td></tr></table>
  <table align="center" border="0" cellpadding="0" cellspacing="0"
         class="r-outlook -outlook pr-16-outlook pl-16-outlook -outlook" role="presentation" style="width:600px;"
         width="600">
    <tr>
      <td style="line-height:0;font-size:0;mso-line-height-rule:exactly;">
  <![endif]-->
  <div class="r pr-16 pl-16"
       style="background: #fffffe; background-color: #fffffe; margin: 0px auto; max-width: 600px;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
           style="background: #fffffe; background-color: #fffffe; width: 100%">
      <tbody>
      <tr>
        <td style="border: none; direction: ltr; font-size: 0; padding: 16px 16px 16px 16px; text-align: left;">
          <!--[if mso | IE]>
          <table role="presentation" border="0" cellpadding="0" cellspacing="0">
            <tr>
              <td class="c-outlook -outlook -outlook" style="vertical-align:middle;width:568px;">
          <![endif]-->
          <div class="xc568 ogf c"
               style="font-size: 0; text-align: left; direction: ltr; display: inline-block; vertical-align: middle; width: 100%;">
            <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                   style="border: none; vertical-align: middle" width="100%">
              <tbody>
              <tr>
                <td align="center" class="c"
                    style="font-size: 0; padding: 0; word-break: break-word;">
                  <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                         style="border-collapse: collapse; border-spacing: 0">
                    <tbody>
                    <tr>
                      <td style="width: 545px">
                        <svg width="100%" height="100%" viewBox="0 0 1440 800" xmlns="http://www.w3.org/2000/svg"
                             style="background-color:#020B1A">
                          <style>
                              .title {{
    fill: #2E82FF;
    font-family: 'Arial Black', sans-serif;
    font-size: 80px;
    font-weight: 900;
                              }}

                              .subtitle {{
    fill: #2E82FF;
    font-family: 'Arial', sans-serif;
    font-size: 36px;
    font-weight: 600;
                              }}
                          </style>
                          <text x="50%" y="45%" text-anchor="middle" class="title">GREG.</text>
                          <text x="50%" y="55%" text-anchor="middle" class="subtitle">Post Sales Reinvented</text>
                        </svg>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
          <!--[if mso | IE]>
          </td></tr></table>
          <![endif]-->
        </td>
      </tr>
      </tbody>
    </table>
  </div>
  <!--[if mso | IE]>
  </td></tr></table>
  <table align="center" border="0" cellpadding="0" cellspacing="0"
         class="r-outlook -outlook pr-16-outlook pl-16-outlook -outlook" role="presentation" style="width:600px;"
         width="600">
    <tr>
      <td style="line-height:0;font-size:0;mso-line-height-rule:exactly;">
  <![endif]-->
  <div class="r pr-16 pl-16"
       style="background: #fffffe; background-color: #fffffe; margin: 0px auto; max-width: 600px;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
           style="background: #fffffe; background-color: #fffffe; width: 100%">
      <tbody>
      <tr>
        <td style="border: none; direction: ltr; font-size: 0; padding: 16px 16px 16px 16px; text-align: left;">
          <!--[if mso | IE]>
          <table role="presentation" border="0" cellpadding="0" cellspacing="0">
            <tr>
              <td class="c-outlook -outlook -outlook" style="vertical-align:middle;width:568px;">
          <![endif]-->
          <div class="xc568 ogf c"
               style="font-size: 0; text-align: left; direction: ltr; display: inline-block; vertical-align: middle; width: 100%;">
            <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
              <tbody>
              <tr>
                <td style="background-color: #fffffe; border: none; vertical-align: middle; padding: 0px 12px 0px 12px;">
                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%">
                    <tbody>
                    <tr>
                      <td align="left" class="x m"
                          style="font-size: 0; padding-bottom: 24px; word-break: break-word;">
                        <div style="text-align: left">
                          <p style="margin: 0; text-align: left; mso-line-height-alt: 24px; mso-ansi-font-size: 16px;">
                            <span style="font-size: 16px; font-family: SF Pro Display, Arial, sans-serif; font-weight: 700; color: #121a26; line-height: 150%; mso-line-height-alt: 24px; mso-ansi-font-size: 16px;">
                              Hey {name}! Your registration is successful 🎉
                            </span>
                          </p>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td align="left" class="x"
                          style="font-size: 0; padding-bottom: 0; word-break: break-word;">
                        <div style="text-align: left">
                          <p style="margin: 0; text-align: left; mso-line-height-alt: 24px; mso-ansi-font-size: 16px;">
                            <span style="font-size: 16px; font-family: Karla, Arial, sans-serif; font-weight: 400; color: #384860; line-height: 150%; mso-line-height-alt: 24px; mso-ansi-font-size: 16px;">
                              We have received your request to join our wait list.
                              We will notify you as soon as we launch.
                            </span>
                          </p>
                          <p style="margin: 0; mso-line-height-alt: 24px; mso-ansi-font-size: 16px;">
                            <span style="font-size: 16px; font-family: Karla, Arial, sans-serif; font-weight: 400; color: #384860; line-height: 150%; mso-line-height-alt: 24px; mso-ansi-font-size: 16px;">
                              If you have any questions, feel free to contact us at info@gregthe.ai
                            </span>
                          </p>
                        </div>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
          <!--[if mso | IE]>
          </td></tr></table>
          <![endif]-->
        </td>
      </tr>
      </tbody>
    </table>
  </div>
  <!--[if mso | IE]>
  </td></tr></table>
  <![endif]-->
</div>
</body>
</html>
"""


def send_email_confirmation_html(first_name: str, verification_url: str) -> str:
    """
    Generates the HTML content for the email verification.

    Args:
        first_name (str): The recipient name.
        verification_url (str): The email verification url.

    Returns:
        str: The HTML content for the email verification.
    """
    return f"""<!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta http-equiv="X-UA-Compatible" content="IE=edge" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
      <link
        href="https://fonts.googleapis.com/css2?family=Inter&display=swap"
        rel="stylesheet"
      />
      <title>Document</title>
    </head>
    <body style="margin: 0px; overflow-x: hidden">
      <div
        style="
          background: url('https://res.cloudinary.com/daviluiz/image/upload/v1636639035/Pattern_Blue_Yellow.png');
          height: 311px;
          width: 100%;
          display: block;
        "
      >
        <center>
          <div>
            <center style="padding-top: 78px">
              <img
                src="https://res.cloudinary.com/daviluiz/image/upload/v1636639053/Logo.png"
                alt="logo"
              />
            </center>
            <h4
              style="
                font-size: 1.5em;
                color: #fff;
                font-family: 'Inter', sans-serif;
                margin-top: 50px;
              "
            >
              Hi,<span
                style="margin-left: 0.5rem; text-transform: capitalize"
              >{first_name}</span>
            </h4>
          </div>
        </center>
      </div>
      
      <hr
        style="
          width: 50%;
          border: 0.5px solid rgb(214, 211, 211);
          margin-top: 2rem;
          margin-bottom: 2rem;
        "
      />
      <center>
        <p
          style="
            text-align: center;
            line-height: 40px;
            color: #515759;
            font-family: 'Inter', sans-serif;
          "
        >
        You are receiving this email because you (or someone else) recently requested to verify this email address.
        <br />
        Please disregard this email if you did not initiate this action.
        </p>
      </center>
      <center>
        <button
          style="
            width: 240px;
            height: 56px;
            background: #1890ff;
            border-radius: 8px;
            margin-top: 21px;
            border: none;
            color: #fff;
            font-size: 18px;
            font-weight: bold;
            font-family: 'Inter', sans-serif;
            cursor: pointer;
          "
        >
        <a style="color: #fff; text-decoration: none;" href="{verification_url}" target="_blank">Verify Email</a>
        </button>
      </center>
    </body>
  </html>
"""
