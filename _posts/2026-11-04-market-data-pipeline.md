---
layout: post
title: "Market Data Pipeline, One Decision at a Time"
description: "How I rebuilt a full day of NASDAQ trading from raw exchange data and tested trading ideas on it, explained one plain-English sentence per decision."
date: 2026-11-04
permalink: /blog/market-data-pipeline/
---

I rebuilt one full day of NASDAQ trading from the exchange's raw data, then used it to test whether simple trading ideas would really have made money.

Every decision below is one sentence, and the code is [on GitHub](https://github.com/LukasUser/market-data-pipeline).

Four words come up a lot: the *order book* is the list of everyone waiting to buy or sell a stock, the *bid* is the best price a buyer is offering, the *ask* is the best price a seller will accept, and the *spread* is the gap between them.

## The data

- I used NASDAQ's raw ITCH feed instead of price charts, because it records every order placed, changed, cancelled and traded.
- I worked from one real trading day, December 30, 2019, which is 268.7 million messages.

## Reading the feed

- I wrote this part in C++ because getting through hundreds of millions of messages has to be fast, and it reads 54.7 million per second.
- I kept only the seven message types that change the order book and counted the rest, so nothing goes missing unnoticed.
- I reject any message with the wrong length rather than guess what it meant.
- I store prices as whole numbers, in ten-thousandths of a dollar, because computers can't store most decimals exactly.

## Rebuilding the order book

- I find orders through a lookup table, because most messages give only an order's ID.
- I keep prices sorted so the best price is always first.
- I give each stock its own book, because every message says which stock it belongs to.
- I report anything that doesn't add up instead of skipping it, such as a message about an order I've never seen.
- I used the closing bell as a test: NASDAQ removes every remaining order at the end of the day, so a correct rebuild must end empty, and all 8,892 stocks did, with zero errors.

## Bringing it into Python

- I connected the C++ to Python, so the fast work stays in C++ and research can be written quickly in Python.
- I kept all the logic in C++, so it only has to be written and tested once.
- I send Python only the moments a stock's best prices change, which turns Apple's 1.5 million messages into about 425,000 updates.

## Testing a first idea

- My first idea was that when far more shares are waiting to buy than to sell, the price is about to rise.
- I measured that before trading on it, and the next move was up 37% of the time when sellers dominated and 64% when buyers did.
- My test makes buyers pay the ask and sellers receive the bid, because that's what trading immediately really costs.
- My test delays each order and fills it at whatever price is there when it arrives, so it can't trade on a price that has already gone.
- The idea was right and still lost 1.36¢ per share, about what it costs to cross the spread.

## Building a matching engine

- To try waiting in line instead of paying to trade immediately, I needed to know each order's exact place in line.
- I keep the orders at each price in arrival order, because exchanges fill first come, first served.
- I made cancelling instant, so an order can leave the middle of the line without disturbing anyone else.
- I threw 20,000 random orders at the engine and checked after each one that no shares appeared or vanished.
- I then compared it with NASDAQ's real trades, and 99.81% of 5.7 million trades hit the order my engine had at the front of the line.
- I don't let the engine decide trades during a replay, because NASDAQ already decided them, and my first version got this wrong and drifted away from the real book.
- I left the remaining 0.19% marked as unexplained, because my one guess turned out to be wrong and I'd rather say so than hide it.

## Waiting in line instead of paying

- I simulated my own order in the real line, where it joins at the back and moves up as orders ahead of it trade or cancel.
- I assumed my orders don't change what anyone else does, which keeps the test simple but isn't fully realistic.
- I split the profit into parts, which showed Apple earned 1.02¢ per share from the spread and lost 1.70¢ within the next second.
- The final result was a loss of 0.69¢ per share, better than 1.36¢ but still a loss, because orders tend to fill just before the price moves against them, which is called adverse selection.
- I tested a slower connection too, and at 1 millisecond instead of 10 microseconds the amount earned from the spread fell to 0.44¢.

## Scaling to 100 stocks

- I split the day into one small file per stock, which took a test on Apple from 133 seconds to 2.8.
- I ran stocks in parallel, because each one can be tested without knowing about the others.
- I save each result the moment it finishes, so a run that gets stopped picks up where it left off.
- I compared stocks by profit per dollar traded, because cents per share makes an $1,800 stock look far more extreme than a $20 one.
- Across the 100 busiest stocks, 39 made money with fast quotes and only 16 with slow ones.

## Keeping it honest

- Every change is automatically built and tested six ways, on Linux and macOS with different compilers, and can't be merged unless all six pass.
- I run the C++ tests under tools that catch memory mistakes that normal tests would miss.
- I work out expected test results by hand, so a test can't simply repeat a bug in the code.
- These results come from one day of data, assume my orders never move the market, and only fill at the best price, so this is a research tool and not a strategy to trade.
