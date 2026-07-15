from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from api.feedback.models import Feedback


@shared_task(bind=True, max_retries=3)
def send_marketing_feedback(self, feedback_id):

    try:

        feedback = Feedback.objects.get(id=feedback_id)

    except Feedback.DoesNotExist:
        
        return

    text_body = f"""
Olá, {feedback.email}!

Recebemos seu feedback com sucesso.

Agradecemos por dedicar um tempo para compartilhar sua opinião conosco. Todo feedback é analisado pela nossa equipe e contribui diretamente para a evolução da Exponere.

Estamos trabalhando para entregar uma plataforma cada vez melhor para nossos usuários.

Obrigado por fazer parte dessa construção!

Atenciosamente,

Equipe Exponere
https://exponere.com.br
"""

    html_body = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Obrigado pelo seu feedback</title>
</head>

<body style="margin:0;padding:40px;background:#f5f5f5;font-family:Arial,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0">
<tr>
<td align="center">

<table width="600" cellpadding="0" cellspacing="0"
style="background:#ffffff;border-radius:12px;overflow:hidden;">

<tr>
<td style="background:#4833AC;padding:36px;text-align:center;">
<h1 style="margin:0;color:#ffffff;">
Exponere
</h1>
</td>
</tr>

<tr>
<td style="padding:40px;color:#333333;">

<h2 style="margin-top:0;">
Olá, {feedback.email}!
</h2>

<p>
Recebemos seu feedback com sucesso.
</p>

<p>
Muito obrigado por compartilhar sua experiência conosco.
</p>

<p>
Cada sugestão, elogio ou crítica é analisado com atenção e nos ajuda a construir uma plataforma cada vez melhor.
</p>

<p>
Sua participação faz parte do crescimento da Exponere.
</p>

<div style="margin:40px 0;text-align:center;">

<a href="https://exponere.com.br"
style="
background:#4833AC;
color:#ffffff;
padding:14px 28px;
border-radius:8px;
text-decoration:none;
font-weight:bold;
display:inline-block;
">
Conhecer a Exponere
</a>

</div>

<p>
Obrigado por fazer parte dessa jornada!
</p>

<p>
Atenciosamente,<br>
<strong>Equipe Exponere</strong>
</p>

</td>
</tr>

<tr>
<td style="
background:#f3f3f3;
padding:18px;
text-align:center;
font-size:12px;
color:#777777;
">
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
        subject="Obrigado pelo seu feedback!",
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[feedback.email],
    )

    message.attach_alternative(html_body, "text/html")
    message.send(fail_silently=False)