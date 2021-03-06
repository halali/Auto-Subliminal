# coding=utf-8

from autosubliminal.notifiers.mail import MailNotifier

notifier_name = 'Mail'

item_dict = {
    'subtitle': 'subtitle',
    'language': 'en',
    'provider': 'provider'
}


def test_mail_disabled():
    notifier = MailNotifier()
    assert notifier.name == notifier_name
    assert notifier.notify_download(**item_dict) is False


def test_mail_exception(monkeypatch):
    monkeypatch.setattr('autosubliminal.NOTIFYMAIL', True)
    monkeypatch.setattr('autosubliminal.MAILFROMADDR', 'from@test.com')
    monkeypatch.setattr('autosubliminal.MAILTOADDR', 'to@test.com')
    monkeypatch.setattr('autosubliminal.MAILSUBJECT', 'subject')
    # Invalid mail server settings patched, so will result in exception
    monkeypatch.setattr('autosubliminal.MAILSRV', 'invalid_server')
    notifier = MailNotifier()
    assert notifier.name == notifier_name
    assert notifier.notify_download(**item_dict) is False


def test_mail_notify_download(monkeypatch, mocker):
    monkeypatch.setattr('autosubliminal.NOTIFYMAIL', True)
    monkeypatch.setattr('autosubliminal.MAILFROMADDR', 'from@test.com')
    monkeypatch.setattr('autosubliminal.MAILTOADDR', 'to@test.com')
    monkeypatch.setattr('autosubliminal.MAILSUBJECT', 'subject')
    monkeypatch.setattr('autosubliminal.MAILSRV', 'server')
    monkeypatch.setattr('autosubliminal.MAILENCRYPTION', 'TLS')
    monkeypatch.setattr('autosubliminal.MAILUSERNAME', 'username')
    monkeypatch.setattr('autosubliminal.MAILPASSWORD', 'password')
    monkeypatch.setattr('autosubliminal.MAILAUTH', None)  # Keep it None because I can't mock it
    mocker.patch('smtplib.SMTP.__init__', return_value=None)
    mocker.patch('smtplib.SMTP.starttls')
    mocker.patch('smtplib.SMTP.ehlo')
    mocker.patch('smtplib.SMTP.login')
    mocker.patch('smtplib.SMTP.sendmail')
    mocker.patch('smtplib.SMTP.quit')
    notifier = MailNotifier()
    assert notifier.name == notifier_name
    assert notifier.notify_download(**item_dict) is True
