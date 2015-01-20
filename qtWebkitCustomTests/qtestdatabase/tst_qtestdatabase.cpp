#include <QString>
#include <QtTest>
#include <QWebView>
#include <QWebFrame>
#include <QWebElement>
#include <QWebPage>
#include <QDir>
#include <QSignalSpy>
#include <QWebSecurityOrigin>
#include <QWebDatabase>

class QtestdatabaseTest : public QObject
{
    Q_OBJECT
    
public:
    QtestdatabaseTest();
    void databaseResult(bool);

private Q_SLOTS:
    void initTestCase();
    void cleanupTestCase();
    void databFunCreate();

private:
    QWebView* m_view;
    QWebPage* m_page;

public slots:
    void testResult(bool);
    void refreshJS();
    QString tmpDirPath() const
    {
        static QString tmpd = QCoreApplication::applicationDirPath() + "/tst_qtestdatabase-"
            + QDateTime::currentDateTime().toString(QLatin1String("yyyyMMddhhmmss"));
        return tmpd;
    }
};

QtestdatabaseTest::QtestdatabaseTest()
{
    qDebug() <<"In QtestdatabaseTest";
}

void QtestdatabaseTest::initTestCase()
{
    m_view = new QWebView();
    m_page = new QWebPage();
}

void QtestdatabaseTest::cleanupTestCase()
{
}

void QtestdatabaseTest::refreshJS()
{
    m_view->page()->mainFrame()->addToJavaScriptWindowObject("myDbTest", this);
}

void QtestdatabaseTest::databFunCreate()
{
//    QString filePath =  QCoreApplication::applicationDirPath();
//    m_view->page()->settings()->setAttribute( QWebSettings::JavascriptEnabled, true );
//    m_view->page()->settings()->enablePersistentStorage(filePath);

//    m_view->load(QUrl("qrc:///some.html"));
    QString path = tmpDirPath();
    m_page->settings()->setOfflineStoragePath(path);
    QVERIFY(m_page->settings()->offlineStoragePath() == path);
    qDebug() << "path:" <<path;

    QWebSettings::setOfflineStorageDefaultQuota(1024 * 1024);
    QVERIFY(QWebSettings::offlineStorageDefaultQuota() == 1024 * 1024);

    m_page->settings()->setAttribute(QWebSettings::LocalStorageEnabled, true);
    m_page->settings()->setAttribute(QWebSettings::OfflineStorageDatabaseEnabled, true);

    QString dbFileName = path + "Databases.db";

    if (QFile::exists(dbFileName))
        QFile::remove(dbFileName);

    m_view->setHtml(QString("<html><head></head><body><div></div></body></html>"));
    m_page->mainFrame()->evaluateJavaScript("var db3; db3=openDatabase('testdb', '1.0', 'test database API', 50000);db3.transaction(function(tx) { tx.executeSql('CREATE TABLE IF NOT EXISTS Test (text TEXT)', []); }, function(tx, result) { }, function(tx, error) { });");
    QTest::qWait(500);

    QWebSecurityOrigin origin = m_page->mainFrame()->securityOrigin();
    QList<QWebDatabase> dbs = origin.databases();
    for (int i = 0; i < dbs.count(); i++) {
        QString fileName = dbs[i].fileName();
        qDebug() << "Database:" << fileName;
        QVERIFY(QFile::exists(fileName));
    }

//    connect(m_view->page()->mainFrame(), SIGNAL(javaScriptWindowObjectCleared()), this, SLOT(refreshJS()));
//    m_view->page()->mainFrame()->addToJavaScriptWindowObject("myDbTest", this);
}

void QtestdatabaseTest::testResult(bool result)
{
    qDebug() << "in testResult" << result;
    QVERIFY2(result,"Failure");
}

QTEST_MAIN(QtestdatabaseTest)

#include "tst_qtestdatabase.moc"
