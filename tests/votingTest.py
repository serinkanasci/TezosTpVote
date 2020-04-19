from os.path import dirname, join
from unittest import TestCase
from decimal import Decimal
from pytezos import ContractInterface,pytezos, format_timestamp, MichelsonRuntimeError

Admin   = "tz1TGu6TN5GSez2ndXXeDX6LgUDvLzPLqgYV"

Alice   = "tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN"
Bob     = "tz1faswCTDciRzE4oJ9jn2Vm2dvjeyA9fUzU"
Vera    = "tz1b7tUupMgCNw2cCLpKTkSD1NZzB5TkP2sv"
Norman  = "tz1ddb9NMYHZi5UzPdzTZMYQQZoMub195zgv"
Margo   = "tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx"
Elias   = "tz1Miko0OWj1rm2GTdTyekr1Jq0noyunzsR7"
Dorie   = "tz1Y6ccjWAe4ai2anCSmSjdKdGFNR4r2mxyJ"
Roselyn = "tz1pyIE15l88X0Xeoaz1AM0rzv7K0ukkJi8z"
Sam     = "tz1nsCEqxqgl4WtX9qgTKJF5I9Y54qdY3uIC"
Leonie  = "tz12FrG4ygXZ5Kq4H6T3T7kC8bztKDHXzuM9"
Randa   = "tz1dTe27jkw925lK61l772qHv626TBvDB7Cu"

class votingTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.voting = ContractInterface.create_from(join(dirname(__file__), '../src/voting.tz'))

    def testAdminVote(self):
        with self.assertRaises(MichelsonRuntimeError):
            self.voting.vote(False).result(
                storage =
                {
                    "votes": { Alice: True },
                    "paused": False,
                    "admin": Admin,
                    "voteCount": 1,
                    "state": ""
                }, source = Admin
            )

    def testVoting(self):
        result = self.voting.vote(True).result(
            storage =
            {
                "votes": { },
                "admin": Admin,
                "paused": False,
                "voteCount": 0,
                "state": ""
            }, source = Bob
        )
        self.assertEqual({ Bob: True }, result.storage["votes"])
        self.assertEqual(False, result.storage["paused"])
        self.assertEqual(1, result.storage["voteCount"])
        self.assertEqual("", result.storage["state"])

    def testDoubleVoting(self):
        with self.assertRaises(MichelsonRuntimeError):
            self.voting.vote(True).result(
                storage =
                {
                    "votes": { Bob: True },
                    "paused": False,
                    "admin": Admin,
                    "voteCount": 1,
                    "state": ""
                }, source = Bob
            )

    def testWin(self):
        result = self.voting.vote(True).result(
            storage =
            {
                "votes": { Bob: True, Vera: True, Norman: True, Margo: True, Elias: True, Dorie: True, Roselyn: False, Sam: False , Leonie: False },
                "paused": False,
                "admin": Admin,
                "voteCount": 9,
                "state": ""
            }, source = Randa
        )
        self.assertEqual("Victoire", result.storage["state"])
        self.assertEqual(True, result.storage["paused"])

    def testLose(self):
        result = self.voting.vote(False).result(
            storage =
            {
                "votes": { Bob: True, Vera: True, Norman: True, Margo: True, Elias: False, Dorie: False, Roselyn: False, Sam: False , Leonie: False },
                "paused": False,
                "admin": Admin,
                "voteCount": 9,
                "state": ""
            }, source = Randa
        )
        self.assertEqual("Defaite", result.storage["state"])
        self.assertEqual(True, result.storage["paused"])

    def testDraw(self):
        result = self.voting.vote(False).result(
            storage =
            {
                "votes": { Bob: True, Vera: True, Norman: True, Margo: True, Elias: True, Dorie: False, Roselyn: False, Sam: False , Leonie: False },
                "paused": False,
                "admin": Admin,
                "voteCount": 9,
                "state": ""
            }, source = Randa
        )
        self.assertEqual("Nul", result.storage["state"])
        self.assertEqual(True, result.storage["paused"])

    def testReset(self):
        result = self.voting.reset(0).result(
            storage =
            {
                "votes": { Bob: True, Vera: True, Norman: True, Margo: True, Elias: True, Dorie: False, Roselyn: False, Sam: False , Leonie: False, Randa: False },
                "admin": Admin,
                "paused": True,
                "voteCount": 10,
                "state": "Nul"
            }, source = Admin
        )
        self.assertEqual({}, result.storage["votes"])
        self.assertEqual(False, result.storage["paused"])
        self.assertEqual(0, result.storage["voteCount"])
        self.assertEqual("", result.storage["state"])

    def testResetUser(self):
        with self.assertRaises(MichelsonRuntimeError):
            self.voting.reset(0).result(
                storage =
                {
                    "votes": { Bob: True, Vera: True, Norman: True, Margo: True, Elias: True, Dorie: False, Roselyn: False, Sam: False , Leonie: False, Randa: False },
                    "admin": Admin,
                    "paused": True,
                    "voteCount": 10,
                    "state": "Nul"
                }, source = Bob
            )

    def testVoteOnPaused(self):
        with self.assertRaises(MichelsonRuntimeError):
            self.voting.vote(True).result(
                storage =
                {
                    "votes": { Bob: True, Vera: True, Norman: True, Margo: True, Elias: True, Dorie: False, Roselyn: False, Sam: False , Leonie: False , Randa: True },
                    "admin": Admin,
                    "paused": True,
                    "voteCount": 10,
                    "state": "Victoire"
                }, source = Alice
            )