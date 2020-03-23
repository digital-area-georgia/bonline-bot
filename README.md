Business Online API Today Activities Bot
========================

ბოტი შექმნილია Business Online API-სთვის. გამოიყენება ყოველდღიური დოკუმენტების წამოსაღებად api/documents/todayactivities ენდფოინთიდან, რომლებშიც 'Credit' ჩანაწერი არ უდრის 0-ს.

API-ს დოკუმენტაცია <https://api.businessonline.ge/>

---------------

**საჭიროებები**:
1. Business Online-ში APISecretKey ტიპის კლიენტის დარეგისტრირება და შესაბამისი უფლებების მინიჭება, რომელიც მოგცემთ client_id-ს და client_secret-ს.
2. ბაზაში დალოგვისთვის MongoDB-ს გამართვა და ConnectionString-ის გენერირება (შეგიძლიათ გამოიყენოთ ლოკალური ან Cloud ბაზა მაგ.: <https://www.mongodb.com/cloud/atlas>)
3. იმ შემთხვევაში თუ გჭირდებათ, რომ ბოტმა "გაფეილების" შემთხვევაში ალერტი გამოაგზავნოს Slack-ში, უნდა დააგენერიროთ Slack-ის აპლიკაციის თოქენი ან თქვენი ანგარიშის legacy-token (<https://api.slack.com/legacy/custom-integrations/legacy-tokens>).

**ნაბიჯები**:

1. pip install -r requirements.txt
2. მთავარ საქაღალდეში უნდა შექმნათ ფაილი *".env"*, სადაც გაწერთ შემდეგ მნიშვნელობებს: client_id, client_secret, grant_type, scope, TokenGenerationEndpoint, DocumentsEndpoint, accountNumber, currency, dbConnStr, dbName, colName, slackerToken, slackerChannel, slackerUsername
3. ტერმინალიდან ვუშვებთ main.py-ს
4. ვუთითებთ ინტერვალის მნიშვნელობას, მაგ. 5
5. ვუთითებთ კი ან არა მნიშვნელობას იმის მიხედვით  გვინდა თუ არა Slack-ში ალერტების მიღება (y/n)

.env ფაილის მაგალითი:

- client_id=
- client_secret=
- grant_type=client_credentials
- scope=read write
- TokenGenerationEndpoint=https://account.bog.ge/auth/realms/bog/protocol/openid-connect/token
- DocumentsEndpoint=https://api.businessonline.ge/api/documents/todayactivities/{accountNumber}/{currency}
- accountNumber=
- currency=
- dbConnStr=
- dbName=
- colName=
- slackerToken=
- slackerChannel=
- slackerUsername=
