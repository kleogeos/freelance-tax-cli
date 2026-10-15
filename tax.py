#!/usr/bin/env python3
import argparse

SS_RATE = 0.124
MEDICARE_RATE = 0.029
NET_EARNINGS_FACTOR = 0.9235  # the 92.35% adjustment baked into Schedule SE


def compute(net_profit, wage_base, additional_medicare_threshold=None):
    base = net_profit * NET_EARNINGS_FACTOR
    ss = min(base, wage_base) * SS_RATE
    medicare = base * MEDICARE_RATE
    additional_medicare = 0.0
    if additional_medicare_threshold is not None and base > additional_medicare_threshold:
        additional_medicare = (base - additional_medicare_threshold) * 0.009
    total = ss + medicare + additional_medicare
    return {
        "net_earnings_for_se_tax": round(base, 2),
        "social_security_tax": round(ss, 2),
        "medicare_tax": round(medicare, 2),
        "additional_medicare_tax": round(additional_medicare, 2),
        "total_se_tax": round(total, 2),
        "deductible_half": round(total / 2, 2),
        "quarterly_payment": round(total / 4, 2),
        "effective_pct_of_profit": round(total / net_profit * 100, 2) if net_profit else 0.0,
    }


def main():
    p = argparse.ArgumentParser(
        prog="freelance-tax",
        description="Estimate US self-employment tax (15.3%) on freelance net profit. Not tax advice.",
    )
    p.add_argument("--net-profit", type=float, required=True, help="Net profit: income minus business expenses")
    p.add_argument("--wage-base", type=float, default=184500, help="Social Security wage base for the current year (default 184500 — verify at irs.gov, it changes yearly)")
    p.add_argument("--additional-medicare-threshold", type=float, default=None, help="If set, also computes the extra 0.9%% Additional Medicare Tax above this threshold (e.g. 200000 for single filers)")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    args = p.parse_args()

    r = compute(args.net_profit, args.wage_base, args.additional_medicare_threshold)

    if args.json:
        import json
        print(json.dumps(r, indent=2))
        return

    print(f"Estimated self-employment tax: ${r['total_se_tax']:,.2f}\n")
    print(f"Net earnings for SE tax (92.35%)   {r['net_earnings_for_se_tax']:,.2f}")
    print(f"Social Security (12.4%)            {r['social_security_tax']:,.2f}")
    print(f"Medicare (2.9%)                     {r['medicare_tax']:,.2f}")
    if args.additional_medicare_threshold is not None:
        print(f"Additional Medicare (0.9% above threshold)  {r['additional_medicare_tax']:,.2f}")
    print(f"Deductible half (line 13, Schedule 1)  {r['deductible_half']:,.2f}")
    print(f"~Quarterly estimated payment         {r['quarterly_payment']:,.2f}")
    print(f"Effective % of net profit            {r['effective_pct_of_profit']:.2f}%")
    print("\nThis excludes federal/state income tax. An estimate, not tax advice — verify with a CPA or irs.gov.")


if __name__ == "__main__":
    main()
