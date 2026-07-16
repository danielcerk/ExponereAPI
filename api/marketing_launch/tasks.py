from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from api.marketing_launch.models import MarketingLaunch


@shared_task(bind=True, max_retries=3)
def send_marketing_launch_campaign(self, lead_id):

    try:

        lead = MarketingLaunch.objects.get(id=lead_id)

    except MarketingLaunch.DoesNotExist:

        return

    campaign = lead.campaign_marketing

    text_body = f"""
Olá, {lead.name}!

Obrigado por solicitar o material:

{campaign.name}

Seu acesso já está liberado.

Para fazer o download, acesse o link abaixo:

{campaign.file_url}

Esperamos que este conteúdo ajude você a melhorar seus resultados.

Se tiver alguma dúvida ou quiser conhecer a plataforma Exponere, estaremos à disposição.

Bom estudo!

Equipe Exponere
https://exponere.com.br
"""

    html_body = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{campaign.name}</title>
</head>

<body style="margin:0;padding:40px;background:#f4f6f8;font-family:Arial,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0">
<tr>
<td align="center">

<table width="620" cellpadding="0" cellspacing="0"
style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 6px 20px rgba(0,0,0,.08);">

<tr>
<td style="background:#4833AC;padding:40px;text-align:center;">

<h1 style="margin:0;color:#ffffff;font-size:30px;">
Exponere
</h1>

<p style="margin:12px 0 0;color:#d8d2ff;font-size:16px;">
Seu material está pronto!
</p>

</td>
</tr>

<tr>
<td style="padding:45px;">

<h2 style="margin-top:0;color:#222;">
Olá, {lead.name}!
</h2>

<p style="font-size:16px;line-height:26px;color:#555;">
Obrigado por preencher nosso formulário.
</p>

<p style="font-size:16px;line-height:26px;color:#555;">
Conforme prometido, seu material já está disponível para download.
</p>

<div style="
background:#f7f7fb;
border-left:4px solid #4833AC;
padding:18px 22px;
margin:30px 0;
">

<h3 style="margin:0;color:#4833AC;">
{campaign.name}
</h3>

<p style="margin-top:10px;color:#666;line-height:24px;">
{campaign.description}
</p>

</div>

<div style="text-align:center;margin:40px 0;">

<a href="{campaign.file_url}"
style="
display:inline-block;
background:#4833AC;
color:#ffffff;
padding:16px 34px;
border-radius:8px;
text-decoration:none;
font-size:16px;
font-weight:bold;
">
⬇ Baixar Material Gratuitamente
</a>

</div>

<p style="font-size:15px;line-height:24px;color:#666;">
Caso o botão acima não funcione, copie e cole o link abaixo no seu navegador:
</p>

<p style="word-break:break-all;">
<a href="{campaign.file_url}" style="color:#4833AC;">
{campaign.file_url}
</a>
</p>

<hr style="margin:40px 0;border:none;border-top:1px solid #eee;">

<p style="font-size:16px;line-height:26px;color:#555;">
Esperamos que este conteúdo seja útil para você.
</p>

<p style="font-size:16px;line-height:26px;color:#555;">
Em breve enviaremos novos materiais gratuitos sobre vendas, CRM, automação e gestão comercial.
</p>

<p style="margin-top:35px;color:#444;">
Até a próxima!
</p>

<p>
<strong>Equipe Exponere</strong>
</p>

</td>
</tr>

<tr>
<td style="
background:#f5f5f5;
padding:25px;
text-align:center;
font-size:12px;
color:#888;
">

Você recebeu este e-mail porque solicitou o material
<strong>{campaign.name}</strong>.

<br><br>

© Exponere • Todos os direitos reservados.

</td>
</tr>

</table>

</td>
</tr>
</table>

</body>
</html>
"""

    message = EmailMultiAlternatives(
        subject=f"Seu material já está disponível: {campaign.name}",
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[lead.email],
    )

    message.attach_alternative(html_body, "text/html")
    message.send()