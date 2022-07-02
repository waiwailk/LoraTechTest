CREATE TABLE "monthly_market_outperformer" (
	"ticker" TEXT NULL DEFAULT NULL,
	"month" INTEGER NULL DEFAULT NULL,
	"tri_return" DOUBLE PRECISION NULL DEFAULT NULL,
	"outperform" BOOLEAN NULL DEFAULT NULL
)
;
COMMENT ON COLUMN "monthly_market_outperformer"."ticker" IS '';
COMMENT ON COLUMN "monthly_market_outperformer"."month" IS '';
COMMENT ON COLUMN "monthly_market_outperformer"."tri_return" IS '';
COMMENT ON COLUMN "monthly_market_outperformer"."outperform" IS '';