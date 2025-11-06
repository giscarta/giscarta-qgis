# -*- coding: utf-8 -*-
"""GISCARTA constants

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""

__author__ = '(C) 2023 GISCARTA'
__date__ = '07/09/2023'
__copyright__ = 'Copyright 2023, GISCARTA'


SIGN_UP_URL = "https://map.giscarta.com/signup"
TOS_URL = 'https://giscarta.com/terms-of-service'
PRIVACY_POLICY_URL = 'https://giscarta.com/privacy-policy'

AUTH_STYLE_MAC = """
QDialog {
    background: transparent;
}

QLineEdit {
    background-color: #294869;
    border-radius: 8px;
    color: white;
    padding: 0px 8px;
    font-size: 13pt;
}

QLabel {
    color: white;
    font-size: 13pt;
}

QPushButton#sign_up_button {
    background-color: rgb(92, 118, 255);
    border: none;
    border-radius: 8px;
    color: white;
    font-weight: bold;
    font-size: 13pt;
    padding: 4px 10px;
}

QPushButton#log_in_button {
    background-color: rgb(0, 204, 164);
    border: none;
    border-radius: 8px;
    color: white;
    font-weight: bold;
    font-size: 13pt;
    padding: 4px 10px;
}

QLabel#footer_label {
}

QLabel#footer_label {
    color: rgb(154, 164, 174);
    font-size: 12pt;
}

QLabel#footer_label a {
    color: rgb(154, 164, 174);
    text-decoration: none; 
}

QLabel#footer_label a:hover {
    color: rgb(180, 190, 200);
    text-decoration: underline;
}

QLabel#footer_label span {
    color: rgb(154, 164, 174);
}

"""

AUTH_STYLE_WIN = """
QDialog {
    background: transparent;
}

QLineEdit {
    background-color: #294869;
    border-radius: 8px;
    color: white;
    padding: 0px 8px;
    font-size: 7pt;
}

QLabel {
    color: white;
    font-size: 7pt;
}

QPushButton#sign_up_button {
    background-color: rgb(92, 118, 255);
    border: none;
    border-radius: 8px;
    color: white;
    font-weight: bold;
    font-size: 7pt;
    padding: 4px 10px;
}

QPushButton#log_in_button {
    background-color: rgb(0, 204, 164);
    border: none;
    border-radius: 8px;
    color: white;
    font-weight: bold;
    font-size: 7pt;
    padding: 4px 10px;
}

QLabel#footer_label {
    color: rgb(154, 164, 174);
    font-size: 6pt;
}

QLabel#footer_label a {
    color: rgb(154, 164, 174);
    text-decoration: none;
}

QLabel#footer_label a:hover {
    color: rgb(180, 190, 200);
    text-decoration: underline;
}

QLabel#footer_label span {
    color: rgb(154, 164, 174);
}
"""

LINK_STYLE = """
a {
    color: blue;
}
"""