from flask_mail import Message
from extensions import mail

def send_reservation_confirmation(email, name, hospital, address, phone, message=None):
    """
    예약 확인 이메일 발송
    """
    if not email:
        return False
    
    subject = f"병원 예약 확인 - {hospital}"
    body = f"""
    안녕하세요, {name}님!

    아래와 같이 병원 예약이 완료되었습니다:

    ▷ 병원: {hospital}
    ▷ 주소: {address}
    ▷ 이름: {name}
    ▷ 연락처: {phone}
    ▷ 요청 사항: {message or "없음"}

    감사합니다!
    """

    try:
        msg = Message(subject=subject, recipients=[email])
        msg.body = body
        mail.send(msg)
        return True
    except Exception as e:
        print(f"이메일 전송 실패: {str(e)}")
        return False