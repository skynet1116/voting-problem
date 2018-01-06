import numpy as np
import math
import time

N = 10000  # population
L = 0.4  # ratio of left-hand people
tax_rate = {0.6: -1, 0.7: -2, 0.8: -3, 0.9: -4, 1: -5}
seed = time.time()
np.random.seed(int(seed))


class People:
    left_hand = None  # bool
    vote = 0  # bool
    tax = 0
    exclude = 0
    payoff = 0

    def __init__(self):
        pass

    def _vote(self, support_rate):
        try:
            self.tax = tax_rate[math.floor(support_rate * 10) / 10] / 2.5
        except:
            self.tax = 0
        self.exclude = 1 - support_rate / (1.000000001 - support_rate)
        self.payoff = self.tax + self.exclude
        prefer = self.exclude / float(self.tax)
        vote = np.random.normal(0.5 * prefer, 0.1)
        self.vote = round(vote)

    def _vote1(self, rt_support, people_count):
        pass

    def __str__(self):
        return '(%d, %d, %d, %f)' % (self.left_hand, self.vote, self.tax, self.exclude)


class LeftHandPeople(People):
    left_hand = 1

    def _vote(self, support_rate):
        try:
            self.tax = tax_rate[math.floor(support_rate * 10) / 10]
        except:
            self.tex = 0
        self.exclude = 1 - support_rate / (1.000000001 - support_rate)
        self.payoff = self.tax + self.exclude
        prefer = self.exclude / float(self.tax)
        vote = np.random.normal(0.5 * prefer, 0.1)
        self.vote = round(vote)

    def _vote1(self, rt_support, people_count):
        if ((1 - rt_support) * people_count + 1) / (people_count + 1) < 0.4:
            self.vote = 1
        else:
            rt_support = (rt_support * people_count + 1) / (people_count + 1)
            self.tax = tax_rate[math.floor(rt_support * 10) / 10]
            self.exclude = 1 - rt_support / (1.000000001 - rt_support)
            if self.tax > self.exclude:
                self.vote = 0
            else:
                self.vote = 1


class RightHandPeople(People):
    left_hand = 0
    vote = 1

    def _vote(self, support_rate):
        pass


def repeated_game(times, support_rate, people):
    s, l, t = [], [], []
    while times > 0:

        for i in people:
            i._vote(support_rate)
            # print(i)

        vote_counter = 0
        L_vote_counter = 0
        total_payoff = 0

        for i in people:
            if i.vote >= 1:
                vote_counter += 1
                if i.left_hand == 1:
                    L_vote_counter += 1
            total_payoff += i.payoff

        support_rate = vote_counter / float(N)
        print("support rate: %.2f \t L-support rate: %.2f \t average total payoff: %.2f" % (
        support_rate, L_vote_counter / (L * N), total_payoff / N))
        s.append(support_rate)
        l.append(L_vote_counter / (L * N))
        t.append(total_payoff / N)
        times -= 1
    print s
    print t
    print l


def real_time_game(people):
    rt_support = 1 - L  # real-time support rate
    vote_counter = 0
    total_payoff = 0
    people_count = 0
    for i in people:
        people_count += 1
        i._vote1(rt_support, people_count)
        if i.vote >= 1:
            vote_counter += 1
        total_payoff += i.payoff
        support_rate = vote_counter / float(people_count)
        print("support rate: %.2f \t average total payoff: %.2f" % (support_rate, total_payoff / people_count))


if __name__ == '__main__':
    people = tuple(
        LeftHandPeople()
        if np.random.rand() > 1 - L  # left-hand rate is L
        else RightHandPeople()
        for i in xrange(N)
    )
    unknow_people = tuple(
        People()
        for i in xrange(N)
    )
    repeated_game(30, 1 - L, unknow_people)
    #real_time_game(people)
