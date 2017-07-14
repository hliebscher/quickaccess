#!/bin/tclsh

load tclrega.so
source [file join $env(DOCUMENT_ROOT) once.tcl]
source [file join $env(DOCUMENT_ROOT) cgi.tcl]



cgi_eval {
	

	cgi_input
	cgi_content_type "text/html; charset=iso-8859-1"
	cgi_http_head

    cgi_html {

		cgi_head {
    		cgi_title "Reboot - HomeMatic QuickAccess"
			puts { <link href="style.css" rel="stylesheet" type="text/css"> }
			puts { <meta name="viewport" content="width=960, initial-zoom=1" /> }
			puts { <meta name="format-detection" content="telephone=no" /> }
			puts { <link rel="apple-touch-icon" href="favicons/icon.png" /> }
			puts { <link rel="icon" href="favicons/icon.png" /> }
			puts { <link rel="shortcut icon" href="favicons/favicon.ico" /> }
			if { ![catch { import app }] } {
				if { $app == "1" } {
					puts { <meta name="mobile-web-app-capable" content="yes" /> }
					puts { <meta name="apple-mobile-web-app-capable" content="yes" /> }
 				}
			}

		}

		cgi_body {

			puts { <script src="style.js" type="text/javascript"></script> }
			puts { <div class="background"></div><div class="page"> }
			puts {<h1>Neustart</h1>}
			
			set pin ""
			catch { import pin }
			set action ""
			catch { import action }

			array set res [rega_script {

				string s_sys_pin = "";
				object o_sys_pin = dom.GetObject ("QuickAccess PIN");
				string s_action = "} $action {";
				
				if (o_sys_pin) { 
					s_sys_pin = o_sys_pin.Value();
				}
				if ((s_sys_pin != "") && (s_sys_pin.ToInteger() != (o_sys_pin.Timestamp().ToInteger() - "} $pin {".ToInteger()))) {
					WriteLine ('<script language="JavaScript">jumpto(\'password.cgi\');</script>');
				} else {

					WriteLine ('<a href="javascript:jumpto(\'index.cgi#\' + js_ianchor);"><div onclick="this.className=\'standard active\';" class="standard button">zur�ck</div></a>');
					if (s_sys_pin != "") {
						WriteLine ('<a href="javascript:jumpto(\'password.cgi?pin=logout\');"><div class="standard button">abmelden</div></a>');
					}

					string stdout = "";
					string stderr = "";

					if (s_action == "") {
						system.Exec ('/usr/bin/uptime', &stdout, &stderr);
						WriteLine ('<p>' # stdout # '</p>');
						WriteLine ('<p>Beim Reboot wird die Konfiguration gespeichert und die Zentrale anschlie�end neu gestartet.</p>');
						WriteLine ('<a href="javascript:jumpto(\'tools_reboot.cgi?action=Reboot\');"><div onclick="this.className=\'standard active\';" class="standard button">Reboot</div></a>');
						WriteLine ('<p>Beim Reset wird die Zentrale neu gestartet, ohne die Konfiguration zu sichern.</p>');
						WriteLine ('<a href="javascript:jumpto(\'tools_reboot.cgi?action=Reset\');"><div onclick="this.className=\'standard active\';" class="standard button">Reset</div></a>');
					} else {

						if ((s_action == "Reboot") || (s_action == "Reset")) {

						WriteLine ('<h3>Achtung!</h3>');
							
							WriteLine ('<p>Die CCU mu� im Normalfall nicht neu gestartet werden. Starten Sie sie nur neu, wenn Sie');
							WriteLine ('ganz genau wissen, was Sie tun! Ein Neustart zum falschen Zeitpunkt kann dazu f�hren, da�');
							WriteLine ('die gesamte Konfiguration fehlerhaft ist und Ihre HomeMatic nicht mehr funktioniert. Im');
							WriteLine ('schlimmsten Fall kann es passieren, da� Sie die CCU zum Hersteller einschicken m�ssen, um');
							WriteLine ('die Systemsoftware neu einspielen zu lassen.<p>');
							WriteLine ('Beim Neustart werden alle Programme getriggert. Starten Sie daher nur neu, wenn Sie anwesend');
							WriteLine ('sind oder genau wissen, was Ihre CCU beim Neustart macht.</p>');
							WriteLine ('<h3>Starten Sie die CCU nur neu, wenn es <b>unbedingt notwendig</b> ist!</h3>');
							WriteLine ('<h3>Sorgen Sie daf�r, da� Sie stets ein <b>aktuelles Backup</b> vorliegen haben, das �ber ');
							WriteLine ('die Backup-Funktion der WebUI erstellt wurde!</h3>');
							
							if (s_action == "Reboot") {
								WriteLine ('<p>Wenn Sie den Reboot ausf�hren, wird die Konfiguration gespeichert');
								WriteLine ('und die Zentrale neu gestartet. Dies dauert unter Umst�nden sehr lange.</p>');
								WriteLine ('<p>Klicken Sie <b>keinesfalls</b> ein zweites Mal auf "Reboot ausf�hren",');
								WriteLine ('w�hrend schon ein Neustart ausgef�hrt wird, da Sie damit Ihre Konfiguration');
								WriteLine ('<b>zerst�ren</b> k�nnen!</p>');
							} else {
								WriteLine ('<p>Wenn Sie den Reset ausf�hren, wird die Zentrale sofort neu gestartet,');
								WriteLine ('ohne die Konfiguration vorher zu sichern.</p>');
							}
							
							WriteLine ('<a href="javascript:jumpto(\'tools_reboot.cgi?action=' # s_action # '_ok\');"><span class="multi_2"><div onclick="this.className=\'standard active\';" class="standard button">' # s_action # '<br>ausf�hren</div></span></a>');
				
							WriteLine ('<p>Wenn Sie auf "' # s_action # ' ausf�hren" klicken, kann der Vorgang nicht abgebrochen werden!</p>');

						}
						
						if (s_action == "Reboot_ok") {
							WriteLine ('<p>Konfiguration sichern ...</p>');
							system.Save();
						}
						if ((s_action == "Reboot_ok") || (s_action == "Reset_ok")) {
							WriteLine ("<p>Neustart!</p>");

							! Vorsicht, system.Exec() macht das System instabil! 
							system.Exec ("/sbin/reboot", &stdout, &stderr);
							! Ahahaha!
						}
						
					}
							
				} ! PIN
					
			}]
	
			puts -nonewline $res(STDOUT)
			
			puts { <p class="footer">QuickAccess (c) 2010-2015 by Yellow Teddybear Software</p> }


		}

    }


}
