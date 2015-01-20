#include <QString>
#include <QtTest>
#include <QWebView>
#include <QWebFrame>
char *s_tdkPath = getenv("TDK_PATH");
class tst_qtestcssfeatures_set4 : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestcssfeatures_set4();
    
private Q_SLOTS:
    void init();
    void cssFunctEmptyCells();
    void cssFunctOutline();
    void cssFunctWhiteSpace();
    void cssFunctUnicodeBidi();
    void cssFunctUnicodeRange();
    void cssFunctPadding();
    void cssFunctBorderSpacing();
    void cssFunctWordSpacing();
    void cssFunctContent();
    void cssFunctBorderWidth();
    void cssFunctOutlineWidth();
    void cssFunctMargin();

private:
    QWebView* m_view;
};


tst_qtestcssfeatures_set4::tst_qtestcssfeatures_set4()
{
}

/*******************
 * To initialize the variables
 * needed to excute the test cases
 *****************/
void tst_qtestcssfeatures_set4::init()
{

}

/*******************
 * Loads a web page with
 * CSS empty cells element
 *****************/

void tst_qtestcssfeatures_set4::cssFunctEmptyCells()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/gcssEmptyCells.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("emptyCell()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("hide"));
}

/*******************
 * Loads a web page with
 * CSS OutlineStyle
 *****************/

void tst_qtestcssfeatures_set4::cssFunctOutline()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/gcssOutline.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyOutline()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY(result.toBool());
}

/*******************
 * Loads a web page with
 * CSS white space
 *****************/

void tst_qtestcssfeatures_set4::cssFunctWhiteSpace()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/gcssWhiteSpace.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("whiteSpace()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("nowrap"));
}

/*******************
 * Loads a web page with
 * CSS unicode bidi
 *****************/

void tst_qtestcssfeatures_set4::cssFunctUnicodeBidi()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/gcssUnicodeBidi.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("unicodeBidi()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("bidi-override"));
}

/*******************
 * Loads a web page with
 * CSS unicode range
 *****************/

void tst_qtestcssfeatures_set4::cssFunctUnicodeRange()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/gcssUnicodeRange.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("unicodeRange()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("U+26"));
}

/*******************
 * Loads a web page with
 * CSS padding
 *****************/

void tst_qtestcssfeatures_set4::cssFunctPadding()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/gcssPadding.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("padding()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("10px"));
}
/*******************
 * Loads a web page with
 * CSS border spacing
 *****************/

void tst_qtestcssfeatures_set4::cssFunctBorderSpacing()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/gcssBorderSpacing.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("borderSpacing()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("10px 10px"));
}

/*******************
 * Loads a web page with
 * CSS word spacing
 *****************/

void tst_qtestcssfeatures_set4::cssFunctWordSpacing()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/gcssWordSpacing.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("wordSpacing()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("30px"));
}

/*******************
 * Loads a web page with
 * CSS content
 *****************/

void tst_qtestcssfeatures_set4::cssFunctContent()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/gcssContent.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyContent()");
    qDebug() << "Getting the result "<< result.toString();
    QVERIFY(result.toBool());
}

/*******************
 * Loads a web page with
 * CSS Border-Width
 *****************/

void tst_qtestcssfeatures_set4::cssFunctBorderWidth()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/gcssBorderWidth.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyBorderWidth()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("5px"));
}

/*******************
 * Loads a web page with
 * CSS Outline-Width
 *****************/

void tst_qtestcssfeatures_set4::cssFunctOutlineWidth()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/gcssOutlineWidth.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyOutlineWidth()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("3px"));
}

/*******************
 * Loads a web page with
 * CSS Margin
 *****************/

void tst_qtestcssfeatures_set4::cssFunctMargin()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/gcssMargin.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("verifyMargin()");
    qDebug() << "Getting the result "<< result.toString();
    QCOMPARE(QString(result.toString()),QString("100px 50px"));
}

QTEST_MAIN(tst_qtestcssfeatures_set4)

#include "tst_qtestcssfeatures_set4.moc"
