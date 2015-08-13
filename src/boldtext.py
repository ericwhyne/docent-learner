# -*- coding: utf-8 -*-
import cgi
import os
import random
import re
import json
import string
import pprint

filesdir = "/var/www/html/docent-learner/boldtext/"
docentlearnerdir = "/var/www/docent-learner/dl/"

length_of_key = 6

html_header = """
<html>
<title>Docent Learner</title>
<link rel="stylesheet" type="text/css" href="/docent-learner/static/style.css">
<body>
"""

questions = [["""In 1848, Charles Burton of New York City made the first baby carriage, but people strongly objected to the vehicles because they said the carriage operators hit too many pedestrians.  Still convinced that he had a good idea, Burton opened a factory in England.  He obtained orders for the baby carriages from Queen Isabella II of Spain, Queen Victoria of England, and the Pasha of Egypt.  The United States had to wait another ten years before it got a carriage factory, and the first year only 75 carriages were sold.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
Even after the success of baby carriages in England,<br> \
<br> \
<input type='hidden' name='question' value='1'> \
<input type='hidden' name='bold' value='false'> \
<input type='radio' name='answer' value='A4'>Charles Burton was a poor man.<br> \
<input type='radio' name='answer' value='B7'>Americans were still reluctant to buy baby carriages.<br> \
<input type='radio' name='answer' value='C9'>Americans purchased thousands of baby carriages.<br> \
<input type='radio' name='answer' value='D1'>the United States bought more carriages than any other country.<br> \
"""],["""In 1848, Charles Burton of New York City made the first baby carriage, but people strongly objected to the vehicles because they said the carriage operators hit too many pedestrians.  Still convinced that he had a good idea, Burton opened a factory in England.  He obtained orders for the baby carriages from Queen Isabella II of Spain, Queen Victoria of England, and the Pasha of Egypt.  The United States had to wait <b>another ten years before it got a carriage factory</b>, and the first year only 75 carriages were sold.
""","""  \
Please select response that best completes the following sentence:<br> \
<br> \
Even after the success of baby carriages in England,<br> \
<br> \
<input type='hidden' name='question' value='1'> \
<input type='hidden' name='bold' value='true'> \
<input type='radio' name='answer' value='A4'>Charles Burton was a poor man.<br> \
<input type='radio' name='answer' value='B7'>Americans were still reluctant to buy baby carriages.<br> \
<input type='radio' name='answer' value='C9'>Americans purchased thousands of baby carriages.<br> \
<input type='radio' name='answer' value='D1'>the United States bought more carriages than any other country.<br> \
"""],["""In the words of Thomas DeQuincey, "It is notorious that the memory strengthens as you lay burdens upon it."  If, like most people, you have trouble recalling the names of those you have just met, try this: the next time you are introduced, plan to remember the names.  Say to yourself, "I'll listen carefully; I'll repeat each person's name to be sure I've got it, and I will remember."  You'll discover how effective this technique is and probably recall those names for the rest of your life.
""",
""" \
Please select response that best completes the following sentence:<br> \
<br> \
The main idea of the paragraph maintains that the memory<br> \
<br> \
<input type='hidden' name='question' value='2'> \
<input type='hidden' name='bold' value='false'> \
<input type='radio' name='answer' value='A4'>always operates at peak efficiency.<br> \
<input type='radio' name='answer' value='B9'>breaks down under great strain.<br> \
<input type='radio' name='answer' value='C7'>improves if it is used often.<br> \
<input type='radio' name='answer' value='D1'>becomes unreliable if it tires.<br> \
"""],["""In the words of Thomas DeQuincey, "It is notorious that the <b>memory strengthens as you lay burdens upon it</b>."  If, like most people, you have trouble recalling the names of those you have just met, try this: the next time you are introduced, plan to remember the names.  Say to yourself, "I'll listen carefully; I'll repeat each person's name to be sure I've got it, and I will remember."  You'll discover how effective this technique is and probably recall those names for the rest of your life.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
The main idea of the paragraph maintains that the memory<br> \
<br> \
<input type='hidden' name='question' value='2'> \
<input type='hidden' name='bold' value='true'> \
<input type='radio' name='answer' value='A4'>always operates at peak efficiency.<br> \
<input type='radio' name='answer' value='B9'>breaks down under great strain.<br> \
<input type='radio' name='answer' value='C7'>improves if it is used often.<br> \
<input type='radio' name='answer' value='D1'>becomes unreliable if it tires.<br> \
"""],["""Unemployment was the overriding fact of life when Franklin D. Roosevelt became President of the United States on March 4, 1933.  An anomaly of the time was that the government did not systematically collect statistics of joblessness; actually it did not start doing so until 1940.  The Bureau of Labor Statistics later estimated that 12,830,000 persons were out of work in 1933, about one-fourth of a civilian labor force of over fifty-one million. <br> \
Roosevelt signed the Federal Emergency Relief Act (FERA) on May 12, 1933.  The President selected Harry L. Hopkins, who headed the New York relief program, to run FERA.  A gifted administrator, Hopkins quickly put the program into high gear.  He gathered a small staff in Washington and brought the state relief organizations into the FERA system.  While the agency tried to provide all the necessities, food came first. City dwellers usually got an allowance for fuel, and rent for one month was provided in case of eviction.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
This passage is primarily about \
<br> \
<input type='hidden' name='question' value='3'> \
<input type='hidden' name='bold' value='false'> \
<input type='radio' name='answer' value='A4'>unemployment in the 1930s.<br> \
<input type='radio' name='answer' value='B9'>the effect of unemployment on United States families.<br> \
<input type='radio' name='answer' value='C1'>President Franklin D. Roosevelt's presidency.<br> \
<input type='radio' name='answer' value='D7'>President Roosevelt's FERA program.<br> \
"""],["""Unemployment was the overriding fact of life when Franklin D. Roosevelt became President of the United States on March 4, 1933.  An anomaly of the time was that the government did not systematically collect statistics of joblessness; actually it did not start doing so until 1940.  The Bureau of Labor Statistics later estimated that 12,830,000 persons were out of work in 1933, about one-fourth of a civilian labor force of over fifty-one million. <br> \
<b>Roosevelt signed the Federal Emergency Relief Act (FERA)</b> on May 12, 1933.  The President selected Harry L. Hopkins, who headed the New York relief program, to run FERA.  A gifted administrator, Hopkins quickly put the program into high gear.  He gathered a small staff in Washington and brought the state relief organizations into the FERA system.  While the agency tried to provide all the necessities, food came first. City dwellers usually got an allowance for fuel, and rent for one month was provided in case of eviction.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
This passage is primarily about <br>\
<br> \
<input type='hidden' name='question' value='3'> \
<input type='hidden' name='bold' value='true'> \
<input type='radio' name='answer' value='A4'>unemployment in the 1930s.<br> \
<input type='radio' name='answer' value='B9'>the effect of unemployment on United States families.<br> \
<input type='radio' name='answer' value='C1'>President Franklin D. Roosevelt's presidency.<br> \
<input type='radio' name='answer' value='D7'>President Roosevelt's FERA program.<br> \
"""],["""It is said that a smile is universally understood.  And nothing triggers a smile more universally than a taste of sugar.  Nearly everyone loves sugar.  Infant studies indicate that humans are born with an innate love of sweets.  Based on statistics, a lot of people in Great Britain must be smiling, because on average, every man, woman and child in that country consumes ninety-five pounds of sugar each year.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
From this passage it seems safe to conclude that the English <br> \
<br> \
<input type='hidden' name='question' value='4'> \
<input type='hidden' name='bold' value='false'> \
<input type='radio' name='answer' value='A4'>do not know that too much sugar is unhealthy.<br> \
<input type='radio' name='answer' value='B9'>eat desserts at every meal.<br> \
<input type='radio' name='answer' value='C7'>are fonder of sweets than most people.<br> \
<input type='radio' name='answer' value='D5'>have more cavities than any other people.<br> \
"""],["""It is said that a smile is universally understood.  And nothing triggers a smile more universally than a taste of sugar.  Nearly everyone loves sugar.  Infant studies indicate that humans are born with an innate love of sweets.  Based on statistics, a lot of people in Great Britain must be smiling, because on average, <b>every man, woman and child in that country consumes ninety-five pounds of sugar</b> each year.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
From this passage it seems safe to conclude that the English <br> \
<br> \
<input type='hidden' name='question' value='4'> \
<input type='hidden' name='bold' value='true'> \
<input type='radio' name='answer' value='A4'>do not know that too much sugar is unhealthy.<br> \
<input type='radio' name='answer' value='B9'>eat desserts at every meal.<br> \
<input type='radio' name='answer' value='C7'>are fonder of sweets than most people.<br> \
<input type='radio' name='answer' value='D5'>have more cavities than any other people.<br> \
"""],["""With varying success, many women around the world today struggle for equal rights.  Historically, women have achieved greater equality with men during periods of social adversity.  Three of the following factors initiated the greatest number of improvements for women:  violent revolution, world war, and the rigors of pioneering in an undeveloped land.  In all three cases, the essential element that improved the status of women was a shortage of men, which required women to perform many of society's vital tasks.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
We can conclude from the information in this passage that <br> \
<br> \
<input type='hidden' name='question' value='5'> \
<input type='hidden' name='bold' value='false'> \
<input type='radio' name='answer' value='A3'>women today are highly successful in winning equal rights.<br> \
<input type='radio' name='answer' value='B9'>only pioneer women have been considered equal to men.<br> \
<input type='radio' name='answer' value='C4'>historically, women have only achieved equality through force.<br> \
<input type='radio' name='answer' value='D7'>historically, the principle of equality alone has not been enough to secure women equal rights.<br> \
"""],["""With varying success, many women around the world today struggle for equal rights.  Historically, women have achieved greater equality with men during periods of social adversity.  Three of the following factors initiated the greatest number of improvements for women:  violent revolution, world war, and the rigors of pioneering in an undeveloped land.  In all three cases, <b>the essential element that improved the status of women was a shortage of men</b>, which required women to perform many of society's vital tasks.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
We can conclude from the information in this passage that <br> \
<br> \
<input type='hidden' name='question' value='5'> \
<input type='hidden' name='bold' value='true'> \
<input type='radio' name='answer' value='A3'>women today are highly successful in winning equal rights.<br> \
<input type='radio' name='answer' value='B9'>only pioneer women have been considered equal to men.<br> \
<input type='radio' name='answer' value='C4'>historically, women have only achieved equality through force.<br> \
<input type='radio' name='answer' value='D7'>historically, the principle of equality alone has not been enough to secure women equal rights.<br> \
"""],["""Please read the following excerpt from "Goffman's Theory of Institutions" by Joseph Ritchie (2014)<br><br>
Sociological inquiry often investigates members of society considered to be on its outer edges. These individuals often live in precarious and vulnerable situations. Traditionally, sociologists have studied these groups to gain insight into the lives of people who are forgotten victims of the blind eye of society. In 1961, Erving Goffman published the book Asylums: Essays on the Social Situation of Mental Patients and Other Inmates. This book outlined the theory of a total institution as seen in prisons and asylums. Goffman's interests and theory helped to reveal the inner mechanics of asylums and the process of institutionalization that takes place within a total institution.<br><br>
According to Goffman's observations and subsequent theories, a total institution seeks to erode the relationships of an individual with the outside world and consume their personal identities and daily activities. The end goal of a total institution is to break down and deconstruct the barriers that separate the spheres of sleep, play, and work in an individual's life by conducting all of these aspects of life in the same location under the same authority. In these institutions, Goffman stated that there is an intentional divide between a large, managed group and a supervisor, which often results in feelings of submissiveness and reluctance to leave the institutionalized setting on the part of the "inmates." This suggests that these restrictive environments lead to the institutionalization of an individual into the group and away from his or her previous, independent life. In these structures, an individual's admission procedures shape and engineer the new member in what may be described as a process of programming. This programming of an individual is characterized by a "leaving off" of one's identity and a "taking on" of one supplied by the establishment. Members of these establishments are alienated from their previous lives and encircled by the ideals and principles of the new institution. A prolonged exposure to similar institutions results in a phenomenon known as "disculturation," which is an un-training that renders an individual temporarily incapable of managing certain features of daily life outside the structures of the institutions. Sociologists often study groups forgotten or ignored by society. Goffman's work illuminated issues with vulnerable populations at asylums and other institutions. Ethnographic field studies have continued this tradition and in doing so have theorized the causes of many of society's ills. Goffman's work is just one example of sociology's ability to delve into an understudied region of society, propose explanations of issues, and theorize possible avenues of reform.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
The supervisor of an institution often produces which of the following feelings in the inmates?<br> \
<br> \
<input type='hidden' name='question' value='6'> \
<input type='hidden' name='bold' value='false'> \
<input type='radio' name='answer' value='A7'>Submissiveness and reluctance to leave<br> \
<input type='radio' name='answer' value='B9'>Anger and frustration<br> \
<input type='radio' name='answer' value='C4'>Confusion and lack of confidence<br> \
<input type='radio' name='answer' value='D3'>Adoration and respect<br> \
<input type='radio' name='answer' value='E6'>Self-contemplation and confusion about one's identity<br> \
"""],["""Please read the following excerpt from "Goffman's Theory of Institutions" by Joseph Ritchie (2014)<br><br>
Sociological inquiry often investigates members of society considered to be on its outer edges. These individuals often live in precarious and vulnerable situations. Traditionally, sociologists have studied these groups to gain insight into the lives of people who are forgotten victims of the blind eye of society. In 1961, Erving Goffman published the book Asylums: Essays on the Social Situation of Mental Patients and Other Inmates. This book outlined the theory of a total institution as seen in prisons and asylums. Goffman's interests and theory helped to reveal the inner mechanics of asylums and the process of institutionalization that takes place within a total institution.<br><br>
According to Goffman's observations and subsequent theories, a total institution seeks to erode the relationships of an individual with the outside world and consume their personal identities and daily activities. The end goal of a total institution is to break down and deconstruct the barriers that separate the spheres of sleep, play, and work in an individual's life by conducting all of these aspects of life in the same location under the same authority. In these institutions, Goffman stated that there is an intentional divide between a large, managed group and a supervisor, which <b>often results in feelings of submissiveness and reluctance to leave</b> the institutionalized setting on the part of the "inmates." This suggests that these restrictive environments lead to the institutionalization of an individual into the group and away from his or her previous, independent life. In these structures, an individual's admission procedures shape and engineer the new member in what may be described as a process of programming. This programming of an individual is characterized by a "leaving off" of one's identity and a "taking on" of one supplied by the establishment. Members of these establishments are alienated from their previous lives and encircled by the ideals and principles of the new institution. A prolonged exposure to similar institutions results in a phenomenon known as "disculturation," which is an un-training that renders an individual temporarily incapable of managing certain features of daily life outside the structures of the institutions. Sociologists often study groups forgotten or ignored by society. Goffman's work illuminated issues with vulnerable populations at asylums and other institutions. Ethnographic field studies have continued this tradition and in doing so have theorized the causes of many of society's ills. Goffman's work is just one example of sociology's ability to delve into an understudied region of society, propose explanations of issues, and theorize possible avenues of reform.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
The supervisor of an institution often produces which of the following feelings in the inmates?<br> \
<br> \
<input type='hidden' name='question' value='6'> \
<input type='hidden' name='bold' value='true'> \
<input type='radio' name='answer' value='A7'>Submissiveness and reluctance to leave<br> \
<input type='radio' name='answer' value='B9'>Anger and frustration<br> \
<input type='radio' name='answer' value='C4'>Confusion and lack of confidence<br> \
<input type='radio' name='answer' value='D3'>Adoration and respect<br> \
<input type='radio' name='answer' value='E6'>Self-contemplation and confusion about one's identity<br> \
"""],["""Please read the following excerpt, adapted from "Narrative in the Life of Frederick Douglass" by Frederick Douglass (1845)<br><br>
I was born in Tuckahoe, near Hillsborough, and about twelve miles from Easton, in Talbot county, Maryland. I have no accurate knowledge of my age, never having seen any authentic record containing it. By far the larger part of the slaves know as little of their ages as horses know of theirs, and it is the wish of most masters within my knowledge to keep their slaves thus ignorant. I do not remember to have ever met a slave who could tell of his birthday. They seldom come nearer to it than planting-time, harvest-time, cherry-time, spring-time, or fall-time. A want of information concerning my own was a source of unhappiness to me even during childhood. The white children could tell their ages. I could not tell why I ought to be deprived of the same privilege. I was not allowed to make any inquiries of my master concerning it. He deemed all such inquiries on the part of a slave improper and impertinent, and evidence of a restless spirit. The nearest estimate I can give makes me now between twenty-seven and twenty-eight years of age. I come to this, from hearing my master say, some time during 1835, I was about seventeen years old.<br><br>
My mother was named Harriet Bailey.  She was the daughter of Isaac and Betsey Bailey, both colored, and quite dark. My mother was of a darker complexion than either my grandmother or grandfather.<br><br>
My father was a white man. He was admitted to be such by all I ever heard speak of my parentage. The opinion was also whispered that my master was my father; but of the correctness of this opinion, I know nothing; the means of knowing was withheld from me. My mother and I were separated when I was but an infant-before I knew her as my mother. It is a common custom, in the part of Maryland from which I ran away, to part children from their mothers at a very early age. Frequently, before the child has reached its twelfth month, its mother is taken from it, and hired out on some farm a considerable distance off, and the child is placed under the care of an old woman, too old for field labor. For what this separation is done, I do not know, unless it be to hinder the development of the child's affection toward its mother, and to blunt and destroy the natural affection of the mother for the child. This is the inevitable result.<br><br>
""",""" \
Please select the best response to the following question.<br> \
<br> \
Who was the author's mother?<br> \
<br> \
<input type='hidden' name='question' value='7'> \
<input type='hidden' name='bold' value='false'> \
<input type='radio' name='answer' value='A9'>A white woman<br> \
<input type='radio' name='answer' value='B7'>Harriet Bailey<br> \
<input type='radio' name='answer' value='C4'>His mother passed away.<br> \
<input type='radio' name='answer' value='D3'>None of the other answers<br> \
<input type='radio' name='answer' value='E6'>Betsey Bailey<br> \
"""],["""Please read the following excerpt, adapted from "Narrative in the Life of Frederick Douglass" by Frederick Douglass (1845)<br><br>
I was born in Tuckahoe, near Hillsborough, and about twelve miles from Easton, in Talbot county, Maryland. I have no accurate knowledge of my age, never having seen any authentic record containing it. By far the larger part of the slaves know as little of their ages as horses know of theirs, and it is the wish of most masters within my knowledge to keep their slaves thus ignorant. I do not remember to have ever met a slave who could tell of his birthday. They seldom come nearer to it than planting-time, harvest-time, cherry-time, spring-time, or fall-time. A want of information concerning my own was a source of unhappiness to me even during childhood. The white children could tell their ages. I could not tell why I ought to be deprived of the same privilege. I was not allowed to make any inquiries of my master concerning it. He deemed all such inquiries on the part of a slave improper and impertinent, and evidence of a restless spirit. The nearest estimate I can give makes me now between twenty-seven and twenty-eight years of age. I come to this, from hearing my master say, some time during 1835, I was about seventeen years old.<br><br>
<b>My mother was named Harriet Bailey.</b>  She was the daughter of Isaac and Betsey Bailey, both colored, and quite dark. My mother was of a darker complexion than either my grandmother or grandfather.<br><br>
My father was a white man. He was admitted to be such by all I ever heard speak of my parentage. The opinion was also whispered that my master was my father; but of the correctness of this opinion, I know nothing; the means of knowing was withheld from me. My mother and I were separated when I was but an infant-before I knew her as my mother. It is a common custom, in the part of Maryland from which I ran away, to part children from their mothers at a very early age. Frequently, before the child has reached its twelfth month, its mother is taken from it, and hired out on some farm a considerable distance off, and the child is placed under the care of an old woman, too old for field labor. For what this separation is done, I do not know, unless it be to hinder the development of the child's affection toward its mother, and to blunt and destroy the natural affection of the mother for the child. This is the inevitable result.<br><br>
""",""" \
Please select the best response to the following question.<br> \
<br> \
Who was the author's mother?<br> \
<br> \
<input type='hidden' name='question' value='7'> \
<input type='hidden' name='bold' value='true'> \
<input type='radio' name='answer' value='A9'>A white woman<br> \
<input type='radio' name='answer' value='B7'>Harriet Bailey<br> \
<input type='radio' name='answer' value='C4'>His mother passed away.<br> \
<input type='radio' name='answer' value='D3'>None of the other answers<br> \
<input type='radio' name='answer' value='E6'>Betsey Bailey<br> \
"""],["""Please read the following excerpt, adapted from "Confessions" by Jean-Jacques Rousseau (trans. 1903)<br><br>
I have entered upon a performance which is without example, whose accomplishment will have no imitator. I mean to present my fellow-mortals with a man in all the integrity of nature; and this man shall be myself.<br><br>
I know my heart, and have studied mankind; I am not made like any one I have been acquainted with, perhaps like no one in existence; if not better, I at least claim originality, and whether Nature did wisely in breaking the mould with which she formed me, can only be determined after having read this work.<br><br>
Whenever the last trumpet shall sound, I will present myself before the sovereign judge with this book in my hand, and loudly proclaim, thus have I acted; these were my thoughts; such was I. With equal freedom and veracity have I related what was laudable or wicked, I have concealed no crimes, added no virtues; and if I have sometimes introduced superfluous ornament, it was merely to occupy a void occasioned by defect of memory: I may have supposed that certain, which I only knew to be probable, but have never asserted as truth, a conscious falsehood. Such as I was, I have declared myself; sometimes vile and despicable, at others, virtuous, generous and sublime; even as thou hast read my inmost soul: Power eternal! assemble round thy throne an innumerable throng of my fellow-mortals, let them listen to my confessions, let them blush at my depravity, let them tremble at my sufferings; let each in his turn expose with equal sincerity the failings, the wanderings of his heart, and, if he dare, aver, I was better than that man.<br><br>
I was born at Geneva in 1712, son of Isaac Rousseau and Susannah Bernard, citizens. My father's share of a moderate competency, which was divided among fifteen children, being very trivial, his business of a watchmaker (in which he had the reputation of great ingenuity) was his only dependence. My mother's circumstances were more affluent; she was daughter of a Mons. Bernard, minister, and possessed a considerable share of modesty and beauty; indeed, my father found some difficulty in obtaining her hand.
""",""" \
Please select the best response to the following question.<br> \
<br> \
What century was the author born in?<br> \
<br> \
<input type='hidden' name='question' value='8'> \
<input type='hidden' name='bold' value='false'> \
<input type='radio' name='answer' value='A9'>Sixteenth<br> \
<input type='radio' name='answer' value='B7'>Eighteenth<br> \
<input type='radio' name='answer' value='C4'>Seventeenth<br> \
<input type='radio' name='answer' value='D3'>None of the other answers<br> \
<input type='radio' name='answer' value='E6'>Twenty-first<br> \
"""],["""Please read the following excerpt, adapted from "Confessions" by Jean-Jacques Rousseau (trans. 1903)<br><br>
I have entered upon a performance which is without example, whose accomplishment will have no imitator. I mean to present my fellow-mortals with a man in all the integrity of nature; and this man shall be myself.<br><br>
I know my heart, and have studied mankind; I am not made like any one I have been acquainted with, perhaps like no one in existence; if not better, I at least claim originality, and whether Nature did wisely in breaking the mould with which she formed me, can only be determined after having read this work.<br><br>
Whenever the last trumpet shall sound, I will present myself before the sovereign judge with this book in my hand, and loudly proclaim, thus have I acted; these were my thoughts; such was I. With equal freedom and veracity have I related what was laudable or wicked, I have concealed no crimes, added no virtues; and if I have sometimes introduced superfluous ornament, it was merely to occupy a void occasioned by defect of memory: I may have supposed that certain, which I only knew to be probable, but have never asserted as truth, a conscious falsehood. Such as I was, I have declared myself; sometimes vile and despicable, at others, virtuous, generous and sublime; even as thou hast read my inmost soul: Power eternal! assemble round thy throne an innumerable throng of my fellow-mortals, let them listen to my confessions, let them blush at my depravity, let them tremble at my sufferings; let each in his turn expose with equal sincerity the failings, the wanderings of his heart, and, if he dare, aver, I was better than that man.<br><br>
<b>I was born at Geneva in 1712</b>, son of Isaac Rousseau and Susannah Bernard, citizens. My father's share of a moderate competency, which was divided among fifteen children, being very trivial, his business of a watchmaker (in which he had the reputation of great ingenuity) was his only dependence. My mother's circumstances were more affluent; she was daughter of a Mons. Bernard, minister, and possessed a considerable share of modesty and beauty; indeed, my father found some difficulty in obtaining her hand.
""",""" \
Please select the best response to the following question.<br> \
<br> \
What century was the author born in?<br> \
<br> \
<input type='hidden' name='question' value='8'> \
<input type='hidden' name='bold' value='true'> \
<input type='radio' name='answer' value='A9'>Sixteenth<br> \
<input type='radio' name='answer' value='B7'>Eighteenth<br> \
<input type='radio' name='answer' value='C4'>Seventeenth<br> \
<input type='radio' name='answer' value='D3'>None of the other answers<br> \
<input type='radio' name='answer' value='E6'>Twenty-first<br> \
"""],["""Please read the following excerpt, adapted from "The Social Contract" by Jean-Jacques Rousseau (1762)<br><br>
Man is born free, yet everywhere he is in chains. One thinks himself the master of others, and still remains a greater slave than they. How did this change come about? I do not know. What can make it legitimate? That question I think I can answer.<br><br>
If I took into account only force, and the effects derived from it, I should say that "as long as a people is compelled to obey, and obeys, it does well; as soon as it can shake off the yoke, and shakes it off, it does still better; for, regaining its liberty by the same right as took it away, either it is justified in resuming it, or there was no justification for those who took it away." But the social order is a sacred right, which is the basis of all other rights. Nevertheless, this right does not come from nature and must therefore be founded on conventions. Before coming to that, I have to prove what I have just asserted.<br><br>
THE FIRST SOCIETIES<br><br>
THE most ancient of all societies, and the only one that is natural, is the family: even so, the children remain attached to the father only so long as they need him for their preservation. As soon as this need ceases, the natural bond is dissolved. The children, released from the obedience they owed to the father, and the father, released from the care he owed his children, return equally to independence. If they remain united, they continue so no longer naturally, but voluntarily; the family itself is then maintained only by convention.
""",""" \
Please select the best response to the following question.<br> \
<br> \
What does the author suggest should be done under the father's governance?<br> \
<br> \
<input type='hidden' name='question' value='9'> \
<input type='hidden' name='bold' value='false'> \
<input type='radio' name='answer' value='A9'>His children must avoid him.<br> \
<input type='radio' name='answer' value='B7'>His children must eventually break free.<br> \
<input type='radio' name='answer' value='C4'>His children must honor and respect him always.<br> \
<input type='radio' name='answer' value='D3'>None of the other answers<br> \
<input type='radio' name='answer' value='E6'>His children can pay him no mind.<br> \
"""],["""Please read the following excerpt, adapted from "The Social Contract" by Jean-Jacques Rousseau (1762)<br><br>
Man is born free, yet everywhere he is in chains. One thinks himself the master of others, and still remains a greater slave than they. How did this change come about? I do not know. What can make it legitimate? That question I think I can answer.<br><br>
If I took into account only force, and the effects derived from it, I should say that "as long as a people is compelled to obey, and obeys, it does well; as soon as it can shake off the yoke, and shakes it off, it does still better; for, regaining its liberty by the same right as took it away, either it is justified in resuming it, or there was no justification for those who took it away." But the social order is a sacred right, which is the basis of all other rights. Nevertheless, this right does not come from nature and must therefore be founded on conventions. Before coming to that, I have to prove what I have just asserted.<br><br>
THE FIRST SOCIETIES<br><br>
THE most ancient of all societies, and the only one that is natural, is the family: even so, the children remain attached to the father only so long as they need him for their preservation. As soon as this need ceases, the natural bond is dissolved. <b>The children, released from the obedience they owed to the father</b>, and the father, released from the care he owed his children, <b>return equally to independence</b>. If they remain united, they continue so no longer naturally, but voluntarily; the family itself is then maintained only by convention.
""",""" \
Please select the best response to the following question.<br> \
<br> \
What does the author suggest should be done under the father's governance?<br> \
<br> \
<input type='hidden' name='question' value='9'> \
<input type='hidden' name='bold' value='true'> \
<input type='radio' name='answer' value='A9'>His children must avoid him.<br> \
<input type='radio' name='answer' value='B7'>His children must eventually break free.<br> \
<input type='radio' name='answer' value='C4'>His children must honor and respect him always.<br> \
<input type='radio' name='answer' value='D3'>None of the other answers<br> \
<input type='radio' name='answer' value='E6'>His children can pay him no mind.<br> \
"""],["""Please read the following excerpt, adapted from "Introductory Remarks" in The Interpretation of Dreams by Sigmund Freud (trans. 1913)<br><br>
In attempting to discuss the interpretation of dreams, I do not believe that I have overstepped the bounds of neuropathological interest. For, when investigated psychologically, the dream proves to be the first link in a chain of abnormal psychic structures whose other links-the hysterical phobia, the obsession, and the delusion-must interest the physician for practical reasons. The dream can lay no claim to a corresponding practical significance; however, its theoretical value is very great, and one who cannot explain the origin of the content of dreams will strive in vain to understand phobias, obsessive and delusional ideas, and likewise their therapeutic importance.<br><br>
While this relationship makes our subject important, it is responsible also for the deficiencies in this work. The surfaces of fracture, which will be frequently discussed, correspond to many points of contact where the problem of dream formation informs more comprehensive problems of psychopathology which cannot be discussed here. These larger issues will be elaborated upon in the future.<br><br>
Peculiarities in the material I have used to elucidate the interpretation of dreams have rendered this publication difficult. The work itself will demonstrate why all dreams related in scientific literature or collected by others had to remain useless for my purpose. In choosing my examples, I had to limit myself to considering my own dreams and those of my patients who were under psychoanalytic treatment. I was restrained from utilizing material derived from my patients' dreams by the fact that during their treatment, the dream processes were subjected to an undesirable complication-the intermixture of neurotic characters. On the other hand, in discussing my own dreams, I was obliged to expose more of the intimacies of my psychic life than I should like, more so than generally falls to the task of an author who is not a poet but an investigator of nature. This was painful, but unavoidable; I had to put up with the inevitable in order to demonstrate the truth of my psychological results at all. To be sure, I disguised some of my indiscretions through omissions and substitutions, though I feel that these detract from the value of the examples in which they appear. I can only express the hope that the reader of this work, putting himself in my difficult position, will show patience, and also that anyone inclined to take offense at any of the reported dreams will concede freedom of thought at least to the dream life.
""",""" \
Please select the best response to the following question.<br> \
<br> \
The author could not rely upon the dreams related in scientific literature because __________.<br> \
<br> \
<input type='hidden' name='question' value='10'> \
<input type='hidden' name='bold' value='false'> \
<input type='radio' name='answer' value='A9'>no work of scientific literature had discussed dreams at the time the author began his study<br> \
<input type='radio' name='answer' value='B6'>he couldn't be sure if material had been changed in or censored from them<br> \
<input type='radio' name='answer' value='C4'>not many dreams had been discussed in scientific literature, and those that had been discussed concerned a very limited number of topics<br> \
<input type='radio' name='answer' value='D3'>he needed to interview people himself in order to discuss their emotional reactions to their dreams<br> \
<input type='radio' name='answer' value='E7'>The author does not give a reason for this in the passage, but says that the rest of his work explains why this is the case.<br> \
"""],["""Please read the following excerpt, adapted from "Introductory Remarks" in The Interpretation of Dreams by Sigmund Freud (trans. 1913)<br><br>
In attempting to discuss the interpretation of dreams, I do not believe that I have overstepped the bounds of neuropathological interest. For, when investigated psychologically, the dream proves to be the first link in a chain of abnormal psychic structures whose other links-the hysterical phobia, the obsession, and the delusion-must interest the physician for practical reasons. The dream can lay no claim to a corresponding practical significance; however, its theoretical value is very great, and one who cannot explain the origin of the content of dreams will strive in vain to understand phobias, obsessive and delusional ideas, and likewise their therapeutic importance.<br><br>
While this relationship makes our subject important, it is responsible also for the deficiencies in this work. The surfaces of fracture, which will be frequently discussed, correspond to many points of contact where the problem of dream formation informs more comprehensive problems of psychopathology which cannot be discussed here. These larger issues will be elaborated upon in the future.<br><br>
Peculiarities in the material I have used to elucidate the interpretation of dreams have rendered this publication difficult. <b>The work itself will demonstrate</b> why all dreams related in scientific literature or collected by others had to remain useless for my purpose. In choosing my examples, I had to limit myself to considering my own dreams and those of my patients who were under psychoanalytic treatment. I was restrained from utilizing material derived from my patients' dreams by the fact that during their treatment, the dream processes were subjected to an undesirable complication-the intermixture of neurotic characters. On the other hand, in discussing my own dreams, I was obliged to expose more of the intimacies of my psychic life than I should like, more so than generally falls to the task of an author who is not a poet but an investigator of nature. This was painful, but unavoidable; I had to put up with the inevitable in order to demonstrate the truth of my psychological results at all. To be sure, I disguised some of my indiscretions through omissions and substitutions, though I feel that these detract from the value of the examples in which they appear. I can only express the hope that the reader of this work, putting himself in my difficult position, will show patience, and also that anyone inclined to take offense at any of the reported dreams will concede freedom of thought at least to the dream life.
""",""" \
Please select the best response to the following question.<br> \
<br> \
The author could not rely upon the dreams related in scientific literature because __________.<br> \
<br> \
<input type='hidden' name='question' value='10'> \
<input type='hidden' name='bold' value='true'> \
<input type='radio' name='answer' value='A9'>no work of scientific literature had discussed dreams at the time the author began his study<br> \
<input type='radio' name='answer' value='B6'>he couldn't be sure if material had been changed in or censored from them<br> \
<input type='radio' name='answer' value='C4'>not many dreams had been discussed in scientific literature, and those that had been discussed concerned a very limited number of topics<br> \
<input type='radio' name='answer' value='D3'>he needed to interview people himself in order to discuss their emotional reactions to their dreams<br> \
<input type='radio' name='answer' value='E7'>The author does not give a reason for this in the passage, but says that the rest of his work explains why this is the case.<br> \
"""]
]

demographics = """<br> \
<br> \
<hr width=350><br> \
Now, please answer some questions about you.<br>\
<br> \
What is your sex?<br> \
<select name='sex'><br> \
<option value='NA'></option><br> \
<option value='Male'>Male</option><br> \
<option value='Female'>Female</option><br> \
</select><br> \
<br> \
In what year were you born? <input type='text' name='year_born'><br> \
<br> \
What is your marital status?<br> \
<select name='marital status'><br> \
<option value='NA'></option><br> \
<option value='Now married'>Now married</option><br> \
<option value='Widowed'>Widowed</option><br> \
<option value='Divorced'>Divorced</option><br> \
<option value='Separated'>Separated</option><br> \
<option value='Never married'>Never married</option><br> \
</select><br> \
<br> \
What is the highest degree or level of school you have completed?<br> \
If currently enrolled, mark the previous grade or highest degree received.<br> \
<select name='education'><br> \
<option value='NA'></option><br> \
<option value='No schooling completed'>No schooling completed</option><br> \
<option value='Nursery school to 8th grade'>Nursery school to 8th grade</option><br> \
<option value='9th, 10th or 11th grade'>9th, 10th or 11th grade</option><br> \
<option value='12th grade, no diploma'>12th grade, no diploma</option><br> \
<option value='High school graduate'>High school graduate - high school diploma or the equivalent (for example: GED)</option><br> \
<option value='Some college credit, but less than 1 year'>Some college credit, but less than 1 year</option><br> \
<option value='1 or more years of college, no degree'>1 or more years of college, no degree</option><br> \
<option value='Associate degree'>Associate degree (for example: AA, AS)</option><br> \
<option value='Bachelor's degree'>Bachelor's degree (for example: BA, AB, BS)</option><br> \
<option value='Master's degree'>Master's degree (for example: MA, MS, MEng, MEd, MSW, MBA)</option><br> \
<option value='Professional degree'>Professional degree (for example: MD, DDS, DVM, LLB, JD)</option><br> \
<option value='Doctorate degree'>Doctorate degree (for example: PhD, EdD)</option><br> \
</select><br> \
<br> \
What is your employment status?<br> \
<select name='employment'><br> \
<option value='NA'></option><br> \
<option value='Employed for wages'>Employed for wages</option><br> \
<option value='Self-employed'>Self-employed</option><br> \
<option value='Out of work and looking for work'>Out of work and looking for work</option><br> \
<option value='Out of work but not currently looking for work'>Out of work but not currently looking for work</option><br> \
<option value='A homemaker'>A homemaker</option><br> \
<option value='A student'>A student</option><br> \
<option value='Retired'>Retired</option><br> \
<option value='Unable to work'>Unable to work</option><br> \
</select><br> \
<br> \
What is your total household income?<br> \
<select name='household income'><br> \
<option value='NA'></option><br> \
<option value='Less than $10,000'>Less than $10,000</option><br> \
<option value='$10,000 to $19,999'>$10,000 to $19,999</option><br> \
<option value='$20,000 to $29,999'>$20,000 to $29,999</option><br> \
<option value='$30,000 to $39,999'>$30,000 to $39,999</option><br> \
<option value='$40,000 to $49,999'>$40,000 to $49,999</option><br> \
<option value='$50,000 to $59,999'>$50,000 to $59,999</option><br> \
<option value='$60,000 to $69,999'>$60,000 to $69,999</option><br> \
<option value='$70,000 to $79,999'>$70,000 to $79,999</option><br> \
<option value='$80,000 to $89,999'>$80,000 to $89,999</option><br> \
<option value='$90,000 to $99,999'>$90,000 to $99,999</option><br> \
<option value='$100,000 to $149,999'>$100,000 to $149,999</option><br> \
<option value='$150,000 or more'>$150,000 or more</option><br> \
</select><br> \
<br> \
Please specify your ethnicity.<br> \
<select name='ethnicity'><br> \
<option value='NA'></option><br> \
<option value='Hispanic or Latino'>Hispanic or Latino</option><br> \
<option value='American Indian or Alaska Native'>American Indian or Alaska Native</option><br> \
<option value='Asian'>Asian</option><br> \
<option value='Black or African American'>Black or African American</option><br> \
<option value='Native Hawaiian or Other Pacific Islander'>Native Hawaiian or Other Pacific Islander</option><br> \
<option value='White'>White</option><br> \
<option value='Other'>Other</option><br> \
</select><br> \
<br> \
What is your primary language (i.e., the language you speak most of the time)?<br> \
<select name='language'><br> \
<option value='NA'></option><br> \
<option value='Rather not say'>Rather not say</option><br> \
<option value='Chinese'>Chinese</option><br> \
<option value='Japanese'>Japanese</option><br> \
<option value='Russian'>Russian</option><br> \
<option value='English'>English</option><br> \
<option value='French'>French</option><br> \
<option value='German'>German</option><br> \
<option value='Spanish'>Spanish</option><br> \
<option value='Danish'>Danish</option><br> \
<option value='Dutch'>Dutch</option><br> \
<option value='Italian'>Italian</option><br> \
<option value='Greek'>Greek</option><br> \
<option value='Portuguese'>Portuguese</option><br> \
<option value='Hebrew'>Hebrew</option><br> \
<option value='Norwegian'>Norwegian</option><br> \
<option value='Swedish'>Swedish</option><br> \
<option value='Korean'>Korean</option><br> \
<option value='Other'>Other</option><br> \
</select><br> \
<br> \
Where are you located?<br> \
<select name='location'><br> \
<option value='NA'></option><br> \
<option value='Africa'>Africa</option><br> \
<option value='Antarctica'>Antarctica</option><br> \
<option value='Asia'>Asia</option><br> \
<option value='Oceania'>Oceania (Australia, New Zealand, etc.)</option><br> \
<option value='Europe'>Europe</option><br> \
<option value='USA'>USA</option><br> \
<option value='Canada'>Canada</option><br> \
<option value='Mexico'>Mexico</option><br> \
<option value='Central America'>Central America</option><br> \
<option value='South America'>South America</option><br> \
<option value='Middle East'>Middle East</option><br> \
<option value='West Indies'>West Indies</option><br> \
</select><br> \
"""

def application(environ, start_response):
  status = '200 OK'
  response_headers = [('Content-type', 'text/html')]
  start_response(status, response_headers)
  form_data = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])
  html = ""
  docentlearner = "<table cellpadding='10'><tr><td><h5><a href='https://github.com/ericwhyne/docent-learner'>Docent-learner</a></h5></td></tr></table>"
  data = {}
  for key in form_data: # convert the FieldStorage to dict
      data[key] = form_data.getvalue(key)
  if len(form_data) > 1:
      turk_random_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length_of_key))
      datafilename = turk_random_key + ".json"
      outfile = open(filesdir + datafilename, "a")
      data['ip'] = environ['REMOTE_ADDR']
      data['turk_random_key'] = turk_random_key
      #outfile.write(str(pprint.pformat(data)))
      outfile.write(json.dumps(data))

      fully_answered = True
      for key in data.keys():
        if data[key] == 'NA':
          fully_answered = False
      if fully_answered:
        html = html_header + "<table class='rounded'><tr><td width=\"400\">Thanks!<br><br>Here's your code for Mechanical Turk:<br> <h1>" + turk_random_key + "</h1></td></tr></table>" + docentlearner
      else:
        html = html_header + "<table class='rounded'><tr><td width=\"400\"><br>Sorry, you failed to enter some requested information. Click back on your browser to try again.<br></td></tr></table>" + docentlearner

  else:
      random_question_i = random.randint(0,len(questions)-1)
      content =  questions[random_question_i][0]
      random_question = questions[random_question_i][1]

      form = """
      <script>
      questionHtml = "<form action=''/docent-learner/dl/boldtext.py' method='post'> \
      <input type='hidden' name='user_agent_id' id='user_agent_id' value=''> \
      <input type='hidden' name='session_id' id='session_id' value=''> \
      %s \
      %s \
      <br><input type='submit' value='Submit'> \
      </form> \
      "
      </script>
      """ % (random_question, demographics)

      content_display = """
      <br><center><table class='imagetable' cellpadding='60'><tr><td id='question_area'>
      """ + content + """
      </td></tr></table><br><br></center>"""

      html = html_header + "<table class='rounded'><tr><td>" + content_display + "</td></tr><tr><td id='button_area'><button type='button' onclick='text_is_read()'>Click here after reading the text</button></td></tr></table>"

      html += docentlearner

      html += form + "<script src='/docent-learner/static/boldtext.js'></script></body></html>"

  return [html]
