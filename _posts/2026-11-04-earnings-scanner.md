---
layout: post
title: "Earnings Scanner, One Decision at a Time"
description: "How I built a program that researches every big company reporting earnings each morning and emails me a summary before the market opens, explained one plain-English sentence per decision."
date: 2026-11-04
permalink: /blog/earnings-scanner/
---

I built a program that wakes up every weekday morning, finds the big companies reporting earnings that day, researches each one, and emails me a short summary before the market opens.

Every decision below is one sentence, and the code is [on GitHub](https://github.com/LukasUser/earnings-scanner).

Four terms come up a lot: an *earnings report* is a company's quarterly results, *EPS* is its profit per share, the *consensus* is the EPS analysts expect, and the *implied move* is how far options prices say the stock could jump when results come out.

## Finding who reports today

- I start from Nasdaq's earnings calendar, because it lists who reports each day, when, and what analysts expect.
- I read the data behind Nasdaq's page instead of the page itself, because it arrives already sorted into clean fields.
- I mark each company as reporting before the market opens or after it closes, because that decides when the stock can react.
- I re-read the previous day's calendar each morning, because by then it shows what companies actually earned.

## Choosing which companies to research

- I skip companies worth less than $300 million, because busy days list hundreds of names and most of them are tiny.
- I research at most 150 companies a day, so the busiest days of earnings season stay manageable.
- I work from largest to smallest, so if time runs out, only the smallest companies are left out.

## Gathering the facts

- I used only free data sources, so the research costs nothing to run.
- From Nasdaq I take analyst expectations, how many analysts raised or cut them lately, ratings, price targets and big investors' positions.
- From Yahoo Finance I take options prices, because they show how big a move the market is actually paying for.
- I compare that implied move with the stock's real moves after its last eight reports, which shows whether the market expects more or less than usual.
- I measure each past move from the right starting point, because a company reporting before the open moves that day and one reporting after the close moves the next.
- I count insider buying and selling over the last 90 days, because executives trading their own stock can be a useful signal.
- I check SEC filings from the last 45 days and flag serious ones, such as restatements, executive departures and cyber incidents.
- I ignore routine filings that just announce results, so a flag always means something.
- I collect a week of news headlines and remove duplicates, because the same story shows up in many places.
- I keep headlines only and not full articles, so nothing downstream can claim more than a title says.
- I research six companies at once but space out my requests to each site, which keeps the run fast without hammering anyone's servers.
- I let each source fail on its own and record what's missing, so one broken website can't ruin the morning.

## Storing everything

- I keep everything in one SQLite database, because a single file needs no server and is easy to copy.
- I save the raw data as well as the cleaned numbers, so I can recalculate things later without fetching them again.
- I save each day separately, so I can look back at what was known on a given morning.

## Asking Claude for a summary

- I have Claude write only after the facts are gathered, and I tell it to use only those facts, so it summarizes my data instead of guessing.
- My first briefs had ten sections each, and I cut them to one sentence, because forty pages isn't something anyone reads over coffee.
- Each sentence is tagged with a mood and how high expectations are, so I can scan a long list quickly.
- I tell Claude never to give buy or sell advice, because the job is to describe the setup and not to make the call.
- I cap it at 40 briefs a day, largest companies first, so the busiest day costs about the same as a quiet one.
- One last call reads the whole list and picks up to five setups that stand out, which is the first thing I read.
- I keep my API key in a private file on my laptop, so it never ends up in the public code.

## Sending the email

- I put a short digest in the email and attach the full report, because Gmail cuts off messages over about 100 KB and the full report is far bigger.
- I send it through my own Gmail account, so I don't need a paid email service.
- I keep my email address and password out of the code too, because the project is public.
- If a run crashes, I get a short failure email instead, so silence never leaves me guessing.

## Reporting yesterday's results

- I first ranked results by how big the surprise was, and the list filled up with nonsense like a +1243% beat.
- That happened because a small or negative estimate makes any percentage huge, so I now show "n/m" for those.
- I now list the 12 largest companies that reported instead, because those are the results people actually care about.
- I calculate each surprise from the numbers on the page, because Nasdaq's own figure once showed a 62% miss for a company that matched expectations exactly.

## Getting it there on time

- I run it at 7:00 every weekday with the scheduler built into macOS, so I don't need to pay for a server.
- My first two emails arrived at 8:07 and 10:17, and the second one came after the market had already opened.
- I assumed slow websites were the cause, but my Mac's power log showed the laptop had been closed and on battery, so it was asleep except for a few seconds at a time.
- The program now tells the Mac to stay awake until it finishes, which works if the laptop is plugged in or open.
- I added a hard stop at 8:50, when it quits researching, sends what it has by 9:00, and says what it skipped.
- That hard stop worked on its first morning: the Mac was asleep again, nine small companies were skipped, and the email went out at 8:52.
- I moved anything the email doesn't need until after it's sent, so it can't hold up the morning.
- I wait for the internet to come back before starting, because a Mac that just woke up can take a moment to reconnect.

## Keeping it honest

- This is a research tool that collects facts and doesn't place trades, and nothing in it is investment advice.
- Nasdaq's and Yahoo's data feeds are unofficial, so they could change or block me without warning.
- Options prices are delayed and can be stale before the open, so implied moves are estimates.
- Many companies report before 7:00, so some briefs describe results that are already out instead of setting them up.
- Nasdaq's EPS can be calculated differently from the estimate it's compared with, so a big miss is worth double-checking.
- Everything depends on one laptop, so a closed Mac on battery still means a thinner report.
