from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from api.launch.models import Launch


@shared_task(bind=True, max_retries=3)
def send_marketing_launch(self, lead_id):
    try:
        lead = Launch.objects.get(id=lead_id)
    except Launch.DoesNotExist:
        return

    text_body = f"""
Olá, {lead.name}!

Obrigado por se cadastrar na lista de espera da Exponere.

Seu interesse foi registrado com sucesso.

Estamos finalizando os últimos detalhes da plataforma e você será um dos primeiros a receber acesso quando o lançamento acontecer.

Enquanto isso, nossa equipe continuará desenvolvendo novos recursos para oferecer uma plataforma completa para gestão de vendas, catálogo digital, CRM e automações.

Até breve!

Equipe Exponere
https://exponere.com.br
"""

    html_body = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
</head>
<body style="margin:0;padding:40px;background:#f5f5f5;font-family:Arial,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0">
<tr>
<td align="center">

<table width="600" cellpadding="0" cellspacing="0"
style="background:#ffffff;border-radius:12px;overflow:hidden;">

<tr>
<td style="background:#4833AC;padding:35px;text-align:center;">
    <h1 style="color:#ffffff;margin:0;">
        Exponere
    </h1>
</td>
</tr>

<tr>
<td style="padding:40px;color:#333333;">

<h2>Olá, {lead.name}!</h2>

<p>
Recebemos seu cadastro na lista de espera da
<strong>Exponere</strong>.
</p>

<p>
Estamos muito felizes pelo seu interesse.
</p>

<p>
Estamos preparando os últimos detalhes para entregar uma plataforma
moderna para gestão de vendas, catálogo digital, CRM e automações.
</p>

<p>
Assim que o lançamento acontecer, você receberá um e-mail em primeira mão.
</p>

<div style="margin:40px 0;text-align:center;">
<a href="https://exponere.com.br"
style="
background:#4833AC;
color:#ffffff;
padding:14px 28px;
text-decoration:none;
border-radius:8px;
display:inline-block;
font-weight:bold;
">
Conhecer a Exponere
</a>
</div>

<p>
Obrigado por fazer parte desse começo.
</p>

<p>
Atenciosamente,<br>
<strong>Equipe Exponere</strong>
</p>

</td>
</tr>

<tr>
<td style="background:#f3f3f3;padding:20px;text-align:center;font-size:12px;color:#777;">
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
        subject="Obrigado pelo seu interesse na Exponere!",
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[lead.email],
    )

    message.attach_alternative(html_body, "text/html")
    message.send()