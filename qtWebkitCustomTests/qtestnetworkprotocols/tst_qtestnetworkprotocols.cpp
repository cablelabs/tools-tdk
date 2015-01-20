#include <QString>
#include <QtTest>
#include "qwebview.h"

class tst_qtestnetworkprotocols : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestnetworkprotocols();
    
private Q_SLOTS:
    void init();
    void nwkpFuncLoadfromftp();
    void nwkpFuncLoadfromftpnegative();
    void nwkpFuncLoadhttppage();
    void nwkpFuncLoadhttpspage();
    void nwkpFuncLoadinvalidhttpsurl();
    void nwkpFuncLoadinvalidhttpurl();

private:
    QWebView *m_view;
};

tst_qtestnetworkprotocols::tst_qtestnetworkprotocols()
{
}

void tst_qtestnetworkprotocols::init()
{
    m_view = new QWebView();
}

void tst_qtestnetworkprotocols::nwkpFuncLoadfromftp()
{
    QUrl url = QUrl("ftp://ftp1.freebsd.org/pub/FreeBSD/README.TXT");
    m_view->load(url);

    QVERIFY2(!url.isEmpty(),"Failure");
    QVERIFY2(url.isValid(),"Failure");
}

void tst_qtestnetworkprotocols::nwkpFuncLoadfromftpnegative()
{
    QUrl url = QUrl("");
    m_view->load(url);

    QVERIFY2(url.isEmpty(),"Failure");
}

void tst_qtestnetworkprotocols::nwkpFuncLoadhttppage()
{
    QUrl url = QUrl("http://qt.digia.com");
    m_view->load(url);

    QVERIFY2(!url.isEmpty(),"Failure");
    QVERIFY2(url.isValid(),"Failure");
}

void tst_qtestnetworkprotocols::nwkpFuncLoadhttpspage()
{
    QUrl url = QUrl("https://www.google.co.in/?gws_rd=cr");
    m_view->load(url);

    QVERIFY2(url.toString().contains("https"),"Failure");
    QVERIFY2(!url.isEmpty(),"Failure");
    QVERIFY2(url.isValid(),"Failure");
}

void tst_qtestnetworkprotocols::nwkpFuncLoadinvalidhttpsurl()
{
      QUrl url = QUrl("https://www.google...co.in/?gws_rd=cr");
      m_view->load(url);

      QVERIFY2(!url.isValid(),"Failure");
}


void tst_qtestnetworkprotocols::nwkpFuncLoadinvalidhttpurl()
{
      QUrl url = QUrl("http://www.google...co.in/?gws_rd=cr");
      m_view->load(url);

      QVERIFY2(!url.isValid(),"Failure");
}

QTEST_MAIN(tst_qtestnetworkprotocols)

#include "tst_qtestnetworkprotocols.moc"
