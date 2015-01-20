#include <QString>
#include <QtTest>
#include <QWebView>
#include <QWebFrame>
char *s_tdkPath = getenv("TDK_PATH");
class tst_qtestcssadvancedfeatures : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestcssadvancedfeatures();
    
private Q_SLOTS:
    void init();
    /* CSS dimension tests */
    void cssFunctDimensionHeight();
    void cssFunctDimensionMaxHeight();
    void cssFunctDimensionMaxWidth();
    void cssFunctDimensionMinHeight();
    void cssFunctDimensionMinWidth();
    void cssFunctDimensionWidth();
    /* CSS display and visibility */
    void cssFunctVisibility();
    void cssFunctDispNone();
    void cssFunctDispInline();
    /* CSS positioning tests */
    void cssFunctPosBottom();
    void cssFunctPosClip();
    void cssFunctPosCursor();
    void cssFunctPosLeft();
    void cssFunctPosOverflow();
    void cssFunctPosPosition();
    void cssFunctPosRight();
    void cssFunctPosTop();
    void cssFunctPosZIndex();
    /* CSS Float tests */
    void cssFunctFloat();
    void cssFunctFloatClear();
    /* CSS Image opacity tests */
    void cssFunctImageOpacity();
    /* CSS Image sprite test */
    void cssFunctImageSpriteHome();
    void cssFunctImageSpritePrev();
    void cssFunctImageSpriteNext();


private:
    QWebView * m_view;
};

tst_qtestcssadvancedfeatures::tst_qtestcssadvancedfeatures()
{
}

void tst_qtestcssadvancedfeatures::init()
{
    m_view = new QWebView;
}

/*****   CSS advanced features - Dimensions  ******/

/* Function to verify CSS dimension - height property */
void tst_qtestcssadvancedfeatures::cssFunctDimensionHeight()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/dimensions.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("dimHeight()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("100px"));

}

/* Function to verify CSS dimension - max height property */
void tst_qtestcssadvancedfeatures::cssFunctDimensionMaxHeight()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/dimMaxHeight.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("dimMaxHeight()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("50px"));

}

/* Function to verify CSS dimension - max width property */
void tst_qtestcssadvancedfeatures::cssFunctDimensionMaxWidth()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/dimMaxWidth.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("dimMaxWidth()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("100px"));

}

/* Function to verify CSS dimension - min height property */
void tst_qtestcssadvancedfeatures::cssFunctDimensionMinHeight()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/dimMinHeight.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("dimMinHeight()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("100px"));

}
/* Function to verify CSS dimension - min width property */
void tst_qtestcssadvancedfeatures::cssFunctDimensionMinWidth()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/dimMinWidth.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("dimMinWidth()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("150px"));

}

/* Function to verify CSS dimension -  width property */
void tst_qtestcssadvancedfeatures::cssFunctDimensionWidth()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/dimensions.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("dimWidth()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("100px"));

}

/*****   CSS advanced features - Display and visibility  ******/

/* Function to verify CSS display - visibility property */
void tst_qtestcssadvancedfeatures::cssFunctVisibility()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/visible.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("hideVisibility()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("hidden"));

}

/* Function to verify CSS display - display:None property */
void tst_qtestcssadvancedfeatures::cssFunctDispNone()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/display.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("disp()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("none"));

}


/* Function to verify CSS display - display:inline property */
void tst_qtestcssadvancedfeatures::cssFunctDispInline()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/displayInline.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("inline()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("inline"));

}
QTEST_MAIN(tst_qtestcssadvancedfeatures)


/*****   CSS advanced features - Positioning  ******/

/* Function to verify CSS positioning - bottom property */
void tst_qtestcssadvancedfeatures::cssFunctPosBottom()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/posBottom.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("posBottom()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Verify if the result is true */
    QVERIFY(result.toBool());

}

/* Function to verify CSS positioning - clip property */
void tst_qtestcssadvancedfeatures::cssFunctPosClip()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/posClip.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("posClip()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Verify if the result is true */
    QVERIFY(result.toBool());

}

/* Function to verify CSS positioning - cursor property */
void tst_qtestcssadvancedfeatures::cssFunctPosCursor()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/posCursor.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("posCursor()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("crosshair"));

}

/* Function to verify CSS positioning - left property */
void tst_qtestcssadvancedfeatures::cssFunctPosLeft()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/posLeft.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("posLeft()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Verify if the result is true */
    QVERIFY(result.toBool());

}

/* Function to verify CSS positioning - overflow property */
void tst_qtestcssadvancedfeatures::cssFunctPosOverflow()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/posOverflow.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("posOverflow()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("scroll"));

}

/* Function to verify CSS positioning - position property */
void tst_qtestcssadvancedfeatures::cssFunctPosPosition()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/posLeft.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("posPosition()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("absolute"));

}
/* Function to verify CSS positioning - right property */
void tst_qtestcssadvancedfeatures::cssFunctPosRight()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/posRight.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("posRight()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Verify if the result is true */
    QVERIFY(result.toBool());


}
/* Function to verify CSS positioning - top property */
void tst_qtestcssadvancedfeatures::cssFunctPosTop()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/posTop.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("posTop()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Verify if the result is true */
    QVERIFY(result.toBool());

}

/* Function to verify CSS positioning - z-index property */
void tst_qtestcssadvancedfeatures::cssFunctPosZIndex()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/poszIndex.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("poszIndex()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Verify if the result is true */
    QVERIFY(result.toBool());

}

/*****   CSS advanced features - Float  ******/

/* Function to verify CSS float property */
void tst_qtestcssadvancedfeatures::cssFunctFloat()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/cssFloat.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("floatProp()");

    /* Get the rright:0px;eturn value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("right"));

}

/* Function to verify CSS float clear property */
void tst_qtestcssadvancedfeatures::cssFunctFloatClear()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/cssFloatClear.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("floatClear()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("both"));

}

/*****   CSS advanced features - Image Opacity  ******/

/* Function to verify CSS Image opacity property */
void tst_qtestcssadvancedfeatures::cssFunctImageOpacity()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/imageOpacity.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("imgOpacity()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("0.6"));

}
/*****   CSS advanced features - Image sprites  ******/

/* Function to verify CSS Image sprite property */
void tst_qtestcssadvancedfeatures::cssFunctImageSpriteHome()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/imageSprites.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("imgSpriteHome()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("http://www.w3schools.com/css/default.asp"));

}

/* Function to verify CSS Image sprite property */
void tst_qtestcssadvancedfeatures::cssFunctImageSpritePrev()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/imageSprites.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("imgSpritePrev()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("http://www.w3schools.com/css/css_intro.asp"));

}

/* Function to verify CSS Image sprite property */
void tst_qtestcssadvancedfeatures::cssFunctImageSpriteNext()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/imageSprites.html";
    /* Select the html file to be read */
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("imgSpriteNext()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("http://www.w3schools.com/css/css_syntax.asp"));

}


#include "tst_qtestcssadvancedfeatures.moc"
