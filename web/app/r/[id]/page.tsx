import Strategy from "@/components/Strategy";
import { StrategyWithProjects } from "@/components/StrategyTable";
import { createSupabaseServerClient } from "@/utils/supabase-server";

export default async function StrategyPage({
  params,
}: {
  params: { id: string };
}) {
  const supabase = createSupabaseServerClient();

  // Fetch the runs for this worker
  const run = await supabase
    .from("runs")
    .select(
      `
      id,
      worker_id,
      created_at,
      prompt,
      strategy_entries(
        *,
        project:projects(*)
      )
    `
    )
    .eq("id", params.id)
    .order("created_at", { ascending: false })
    .single();

  if (run.error || !run.data) {
    console.error(run.error);
    throw Error(`Runs with id ${params.id} not found.`);
  }

  const data = run.data.strategy_entries as unknown as StrategyWithProjects;

  return (
    <Strategy
      strategy={data.map((s) => ({
        ...s,
        selected: true,
      }))}
      prompt={run.data.prompt}
      runId={run.data.id}
    />
  );
}
